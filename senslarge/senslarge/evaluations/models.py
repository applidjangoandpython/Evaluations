import uuid

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string

from ordered_model.models import OrderedModel


class Formulaire(models.Model):
    POND = 'PONDERATION'
    SELECT = 'SELECTION'
    SELECT_VAL = 'SELECTION_VALORISATION'
    TYPES = [
        (POND, 'Ponderation'),
        (SELECT, 'Selection'),
        (SELECT_VAL, 'Selection and Valorisation')
    ]
    titre = models.CharField(max_length=200, verbose_name="Titre")
    introduction = models.TextField(verbose_name="Introduction")
    type_form = models.CharField(
        choices=TYPES, max_length=26, verbose_name="Type"
    )
    nb_points = models.IntegerField(
        default=0,
        verbose_name="Nombre de points",
        help_text="À répartir entre les choix",
    )

    BARRE = 'radar'
    SELECT = 'barres'
    GRAPH = [
        (BARRE, 'radar'),
        (SELECT, 'barres')
    ]
    typegraphe = models.CharField(
        choices=GRAPH, max_length=7, verbose_name="Graphique"
    )

    def __str__(self):
        return self.titre


class Question(OrderedModel):
    question_text = models.TextField(verbose_name="Texte")
    formulaire = models.ForeignKey(
        'Formulaire',
        related_name="questions",
        on_delete=models.CASCADE,
        verbose_name="Formulaire",
    )

    order_with_respect_to = 'formulaire'

    class Meta:
        ordering = ('formulaire', 'order')

    def __str__(self):
        return self.question_text


class Choice(OrderedModel):
    choice_text = models.TextField(
        blank=True, verbose_name="Texte"
    )
    question = models.ForeignKey(
        'Question',
        related_name="choices",
        on_delete=models.CASCADE,
        verbose_name="Question",
    )
    categorie = models.ForeignKey(
        'Categorie',
        related_name="choixcategories",
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Catégorie",
    )
    VALPLUS0 = '0'
    VALPLUS1 = '+1'
    VALPLUS2 = '+2'
    VALPLUS3 = '+3'
    VALMOINS1 = '-1'
    VALMOINS2 = '-2'
    VALMOINS3 = '-3'
    VAL = [
        (VALPLUS0, '0'),
        (VALPLUS1, '+1'),
        (VALPLUS2, '+2'),
        (VALPLUS3, '+3'),
        (VALMOINS1, '-1'),
        (VALMOINS2, '-2'),
        (VALMOINS3, '-3')
    ]
    valorisation = models.CharField(
        default=0, choices=VAL, max_length=2, verbose_name="Valorisation"
    )

    order_with_respect_to = 'question'

    class Meta:
        ordering = ('question', 'order')


class Categorie(models.Model):
    categorie_text = models.TextField(
        max_length=200, blank=True, verbose_name="Texte"
    )
    formulaire = models.ForeignKey(
        'Formulaire',
        related_name="categories",
        on_delete=models.CASCADE,
        verbose_name="Formulaire",
    )

    def __str__(self):
        return self.categorie_text


class ChoiceUtilisateur(models.Model):
    reference_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    reference_choice = models.ForeignKey(
        'Choice',
        related_name="choiceusers",
        on_delete=models.CASCADE
    )
    valeur_entier = models.IntegerField(default=0)


class TicketFormulaire(models.Model):
    formul = models.ManyToManyField(
        'Formulaire',
        related_name="tickets"
    )
    users_lien = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="formulaires",
    )
    token = models.UUIDField(
        default=uuid.uuid4, editable=False
    )

    def send_to_user(self, request):
        url_formulaire = reverse(
            'evaluations:introduction_formulaire', kwargs={
                'token': str(self.token)
            }
        )
        url = request.build_absolute_uri(url_formulaire)

        txt_message = render_to_string(
            'evaluations/emails/ticket_utilisateur/body.txt',
            {'object': self, 'url': url}
        )
        html_message = render_to_string(
            'evaluations/emails/ticket_utilisateur/body.html',
            {'object': self, 'url': url}
        )
        send_mail(
            'Votre évaluation Sens Large',
            txt_message,
            settings.DEFAULT_FROM_EMAIL,
            [self.users_lien.email],
            html_message=html_message
        )


class FormUser:
    def __init__(self, form, user):
        self.form = form
        self.user = user

    def header(self):
        return self.form.categories.order_by('pk').values_list(
            'categorie_text', flat=True
        )

    def rows(self):
        if self.form.type_form == self.form.SELECT_VAL:
            yield from self.rows_select_val()
            return
        for question in self.form.questions.all():
            choix = (
                ChoiceUtilisateur.objects.filter(
                    reference_user=self.user,
                    reference_choice__question=question
                )
                .order_by('reference_choice__categorie__pk')
            )
            yield question, choix

    def rows_select_val(self):
        for question in self.form.questions.all():
            choices = []
            for choice in question.choices.order_by('categorie__pk'):
                choices.append((choice, ChoiceUtilisateur.objects.filter(
                    reference_user=self.user,
                    reference_choice=choice
                ).exists()))
            print(question, choices)
            yield question, choices

    def footer(self):
        row = []
        if self.form.type_form == self.form.SELECT_VAL:
            return self.footer_select_val()

        for question, choices in self.rows():
            row_started = bool(row)
            for i, choice in enumerate(choices):
                if not row_started:
                    row.append(choice.valeur_entier)
                else:
                    row[i] += choice.valeur_entier
        return row

    def footer_select_val(self):
        row = []
        for question, choices in self.rows():
            row_started = bool(row)
            for i, choice in enumerate(choices):
                if not row_started:
                    row.append(choice[1] and 1 or 0)
                else:
                    row[i] += choice[1] and 1 or 0
        return row

    def footer_select_val_sum(self):
        row = [0 for c in self.form.categories.all()]
        for question in self.form.questions.all():
            qs = question.choices.order_by('categorie__pk')
            for i, choice in enumerate(qs):
                user_choice = ChoiceUtilisateur.objects.filter(
                    reference_user=self.user,
                    reference_choice=choice
                ).first()
                if user_choice:
                    if choice.valorisation[0] == '+':
                        row[i] += int(choice.valorisation[1])
                    else:
                        row[i] += int(choice.valorisation)
        return row

    def performance(self):
        return sum(self.footer_select_val_sum())
