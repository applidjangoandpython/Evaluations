import pytest
from django.shortcuts import reverse
from senslarge.evaluations.models import Formulaire

pytestmark = pytest.mark.django_db


def test_detail_repondant_pond(admin_client, formulaire_factory,
                               user_factory, question_factory,
                               categorie_factory, choice_factory,
                               choiceutilisateur_factory):
    form = formulaire_factory(
        type_form=Formulaire.POND,
        typegraphe=Formulaire.BARRE
    )
    user = user_factory(
        first_name="Ham",
        last_name="James",
        email="hamadybarry32@yahoo.fr"
    )
    question = question_factory(
        question_text="question_text",
        formulaire=form
    )
    categorie1 = categorie_factory(
        categorie_text="categorie_test",
        formulaire=form
    )
    categorie2 = categorie_factory(
        categorie_text="test",
        formulaire=form
    )
    categorie3 = categorie_factory(
        categorie_text="test",
        formulaire=form
    )
    categorie4 = categorie_factory(
        categorie_text="test",
        formulaire=form
    )
    choice1 = choice_factory(
        choice_text="test",
        question=question,
        categorie=categorie1
    )
    choice2 = choice_factory(
        choice_text="test",
        question=question,
        categorie=categorie2
    )
    choice3 = choice_factory(
        choice_text="test",
        question=question,
        categorie=categorie3
    )
    choice4 = choice_factory(
        choice_text="test",
        question=question,
        categorie=categorie4
    )
    choiceutilisateur_factory(
        reference_user=user,
        reference_choice=choice1,
        valeur_entier=0
    )
    choiceutilisateur_factory(
        reference_user=user,
        reference_choice=choice2,
        valeur_entier=0
    )
    choiceutilisateur_factory(
        reference_user=user,
        reference_choice=choice3,
        valeur_entier=0
    )
    choiceutilisateur_factory(
        reference_user=user,
        reference_choice=choice4,
        valeur_entier=0
    )
    response = admin_client.get(
            reverse(
                'evaluations:repondant',
                kwargs={'formulaire_pk': form.pk, 'user_pk': user.pk}
            )
    )

    assert response.status_code == 200


def test_detail_repondant_select_val(admin_client, user, formulaire_factory,
                                     categorie_factory, question_factory,
                                     choice_factory,
                                     choiceutilisateur_factory):
    form = formulaire_factory(
        titre='Les styles de management',
        type_form=Formulaire.SELECT_VAL,
        typegraphe=Formulaire.BARRE
    )

    cat1 = categorie_factory(formulaire=form)
    cat2 = categorie_factory(formulaire=form)
    cat3 = categorie_factory(formulaire=form)
    cat4 = categorie_factory(formulaire=form)

    question1 = question_factory(formulaire=form)
    question2 = question_factory(formulaire=form)
    choice1 = choice_factory(
        question=question1,
        categorie=cat1
    )
    choice_factory(
        question=question1,
        categorie=cat2
    )
    choice_factory(
        question=question1,
        categorie=cat3
    )
    choice_factory(
        question=question1,
        categorie=cat4
    )
    choice2 = choice_factory(
        question=question2,
        categorie=cat1
    )
    choice_factory(
        question=question2,
        categorie=cat2
    )
    choice_factory(
        question=question2,
        categorie=cat3
    )
    choice_factory(
        question=question2,
        categorie=cat4
    )
    choiceutilisateur_factory(
        reference_user=user,
        reference_choice=choice1,
        valeur_entier=0
    )
    choiceutilisateur_factory(
        reference_user=user,
        reference_choice=choice2,
        valeur_entier=0
    )

    response = admin_client.get(
            reverse(
                'evaluations:repondant',
                kwargs={'formulaire_pk': form.pk, 'user_pk': user.pk}
            )
    )

    assert response.status_code == 200


def test_detail_repondant_no_admin(client, formulaire, user):
    url = reverse(
        'evaluations:repondant',
        kwargs={'formulaire_pk': formulaire.pk, 'user_pk': user.pk}
    )
    response = client.get(url)

    assert response.status_code == 302
    assert response['Location'].startswith(reverse('evaluations:login'))
