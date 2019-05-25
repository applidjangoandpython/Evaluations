import factory

from factory import SubFactory, Sequence
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from .models import (
    Formulaire,
    Question,
    Categorie,
    Choice,
    ChoiceUtilisateur,
    TicketFormulaire
)


class FormulaireFactory(DjangoModelFactory):
    titre = Sequence(lambda n: 'Titre {0}'.format(n))
    introduction = Sequence(lambda n: 'Intro {0}'.format(n))
    nb_points = 10

    class Meta:
        model = Formulaire


class QuestionFactory(DjangoModelFactory):
    question_text = Sequence(lambda n: 'Question test {0}'.format(n))
    formulaire = SubFactory(FormulaireFactory)

    class Meta:
        model = Question


class CategorieFactory(DjangoModelFactory):
    categorie_text = Sequence(lambda n: 'Categorie test {0}'.format(n))
    formulaire = SubFactory(FormulaireFactory)

    class Meta:
        model = Categorie


class ChoiceFactory(DjangoModelFactory):
    choice_text = Sequence(lambda n: 'Choice test {0}'.format(n))
    question = SubFactory(QuestionFactory)
    categorie = SubFactory(CategorieFactory)

    class Meta:
        model = Choice


class UserFactory(DjangoModelFactory):

    class Meta:
        model = User


class ChoiceutilisateurFactory(DjangoModelFactory):
    reference_user = SubFactory(UserFactory)
    reference_choice = SubFactory(ChoiceFactory)
    valeur_entier = 10

    class Meta:
        model = ChoiceUtilisateur


class TicketFactory(DjangoModelFactory):
    users_lien = SubFactory(UserFactory)

    class Meta:
        model = TicketFormulaire

    @factory.post_generation
    def formul(self, create, extracted, **kwargs):
        for fromulaire in extracted:
            self.formul.add(fromulaire)
