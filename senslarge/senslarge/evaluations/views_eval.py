from django.shortcuts import HttpResponseRedirect
from django.views.generic import ListView, FormView, RedirectView
from django.urls import reverse, reverse_lazy
from django import forms
from django.http import Http404
from django.contrib.auth import login
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User

from .models import (
    Choice,
    Question,
    ChoiceUtilisateur,
    Formulaire,
    TicketFormulaire
)

from .forms import UserChoiceForm
from .mixins import LoginRequired
from .views_mgmt import Creation_PDF


class Root(LoginRequired, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return reverse('evaluations:home')

        if self.request.user.formulaires:
            return reverse('evaluations:introduction_formulaire', kwargs={
                'token': self.request.user.formulaires.token
            })

        raise PermissionDenied()


class Accueil(LoginRequired, ListView):
    model = Formulaire
    template_name = 'evaluations/introductionformulaire.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        exclude_clause = {
            "questions__choices__choiceusers__reference_user":
            self.request.user
        }
        queryset = (
            queryset.filter(tickets__users_lien=self.request.user)
            .exclude(**exclude_clause)
            .distinct()
        )
        return queryset


class TokenEntryPoint(RedirectView):
    url = reverse_lazy('evaluations:accueil')

    def get_redirect_url(self, *args, **kwargs):
        token = self.kwargs['token']
        try:
            ticket = TicketFormulaire.objects.get(token=token)
        except Exception:
            raise Http404()
        user = ticket.users_lien
        login(self.request, user)
        return super().get_redirect_url(*args, **kwargs)


class Repondre_Question(LoginRequired, FormView):
    model = ChoiceUtilisateur
    template_name = 'evaluations/repondre_question.html'

    def get_form_kwargs(self):
        context_form = super().get_form_kwargs()
        if self.get_formulaire().type_form == Formulaire.POND:
            context_form['my_formulaire'] = Formulaire.objects.get(
                pk=self.kwargs['formulaire_pk']
            )
        return context_form

    def get_formulaire(self):
        return Formulaire.objects.get(pk=self.kwargs['formulaire_pk'])

    def get_question(self):
        return Question.objects.get(pk=self.kwargs['question_pk'])

    def get_form_class(self):
        formulaire = self.get_formulaire()
        question = self.get_question()
        fields = {}
        if formulaire.type_form == Formulaire.POND:
            for choice in question.choices.all():
                fields[str(choice.pk)] = forms.IntegerField(
                    label=choice.choice_text,
                    max_value=formulaire.nb_points,
                    min_value=0
                )
            return type('Monform', (UserChoiceForm,), fields)

        choices = []
        for choice in question.choices.all():
            choices.append((choice.pk, choice.choice_text))

        for choix in question.choices.all():
            fields[str(choice.pk)] = forms.ChoiceField(
                widget=forms.RadioSelect,
                choices=choices,
                label='',
            )
        return type('Monform', (forms.Form,), fields)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = Question.objects.get(
            pk=self.kwargs['question_pk']
        )
        return context

    def get_success_url(self):
        formulaire = self.get_formulaire()
        choix_repondus = ChoiceUtilisateur.objects.filter(
            reference_user=self.request.user
        ).values_list('reference_choice')
        question_non_repondus = formulaire.questions.exclude(
            choices__in=choix_repondus
        )
        if question_non_repondus:
            return reverse('evaluations:repondre_question', kwargs={
                    'formulaire_pk': formulaire.pk,
                    'question_pk': question_non_repondus.first().pk
                }
            )
        view = Creation_PDF()
        view.request = self.request
        view.kwargs = dict(
            formulaire_pk=formulaire.pk,
            user_pk=self.request.user.pk
        )
        response = view.get(None)
        pdf_content = response.get_document()
        mon_pdf = pdf_content.write_pdf()

        subject = 'Reponse de {} {} pour {}'.format(
            self.request.user.first_name,
            self.request.user.last_name,
            formulaire.titre
        )
        to = User.objects.filter(is_superuser=True).values_list(
            'email', flat=True
        )
        message = EmailMessage(
            subject,
            '',
            settings.DEFAULT_FROM_EMAIL,
            to,
        )
        message.attach(
            '{}_{}.pdf'.format(self.request.user.username, formulaire.pk),
            mon_pdf,
            'application/pdf'
        )
        message.send(fail_silently=True)

        exclude_clause = {
            "questions__choices__choiceusers__reference_user":
            self.request.user
        }
        next_form = (
            Formulaire.objects
            .filter(tickets__users_lien=self.request.user)
            .exclude(**exclude_clause)
            .distinct()
            .first()
        )

        if next_form:
            return reverse('evaluations:accueil')

        return reverse('evaluations:conclusion')

    def form_valid(self, form):
        for choice_id, value in form.cleaned_data.items():
            ChoiceUtilisateur.objects.create(
                    reference_user=self.request.user,
                    reference_choice=Choice.objects.get(pk=choice_id),
                    valeur_entier=value
            )
        return HttpResponseRedirect(self.get_success_url())


class Conclusion(LoginRequired, ListView):
    model = ChoiceUtilisateur
    template_name = 'evaluations/conclusion.html'
