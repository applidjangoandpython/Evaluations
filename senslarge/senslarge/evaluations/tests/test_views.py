import uuid

import pytest
from django.core import mail
from django.shortcuts import reverse
from senslarge.evaluations.models import (
    Formulaire,
    Choice,
    ChoiceUtilisateur
)

pytestmark = pytest.mark.django_db


def test_list_formulaire_admin(admin_client, formulaire_factory):
    formulaire_factory(
        type_form=Formulaire.SELECT_VAL,
        typegraphe=Formulaire.BARRE
    )
    formulaire_factory(
        type_form=Formulaire.SELECT,
        typegraphe=Formulaire.BARRE
    )

    response = admin_client.get(reverse('evaluations:liste_formulaire'))

    assert response.status_code == 200

    assert response.context_data['nombre'] == 2


def test_list_formulaire_no_admin(client, formulaire_factory):
    formulaire_factory(
        type_form=Formulaire.POND,
        typegraphe=Formulaire.BARRE
    )
    formulaire_factory(
        type_form=Formulaire.SELECT,
        typegraphe=Formulaire.BARRE
    )

    response = client.get(reverse('evaluations:liste_formulaire'))

    assert response.status_code == 302
    assert reverse('evaluations:login') in response.url


def test_list1_formulaire_admin(admin_client, formulaire_factory):
    formulaire_factory(
        type_form=Formulaire.SELECT_VAL,
        typegraphe=Formulaire.BARRE
    )

    response = admin_client.get(reverse('evaluations:liste_formulaire'))

    assert response.status_code == 200

    assert response.context_data['nombre'] == 1


def test_list1_formulaire_no_admin(client, formulaire_factory):
    formulaire_factory(
        type_form=Formulaire.SELECT_VAL,
        typegraphe=Formulaire.BARRE
    )

    response = client.get(reverse('evaluations:liste_formulaire'))

    assert response.status_code == 302

    assert reverse('evaluations:login') in response.url


def test_intro_formulaire_admin(admin_client, formulaire_factory,
                                ticket_factory, user_factory,
                                question_factory):

    form = formulaire_factory(
            type_form=Formulaire.SELECT_VAL,
            typegraphe=Formulaire.BARRE
    )
    question_factory(
        question_text="question_text",
        formulaire=form
    )
    user = user_factory(
        first_name="Ham",
        last_name="James",
        email="hamady@hashbang.fr"
    )
    ticket = ticket_factory(
        users_lien=user,
        formul=[form]
    )
    response = admin_client.get(reverse(
        'evaluations:introduction_formulaire',
        kwargs={'token': ticket.token}
    ))
    assert response.status_code == 302
    assert response['Location'] == reverse('evaluations:accueil')


def test_intro_formulaire_mauvais_token_admin(admin_client):
    response = admin_client.get(reverse(
        'evaluations:introduction_formulaire',
        kwargs={'token': 'cnhf215kff45d4ffdq5q'}
    ))
    assert response.status_code == 404


def test_creation_repondant_admin(admin_client, formulaire_factory):

    form = formulaire_factory(
            type_form=Formulaire.SELECT_VAL,
            typegraphe=Formulaire.BARRE
    )

    response = admin_client.post(
        reverse('evaluations:creation_repondant'),
        {
            'first_name': 'ham',
            'last_name': 'James',
            'email': 'hamady@hashbang.fr',
            'formulaires': [form.pk]
        }
    )
    assert response.status_code == 302

    assert response['Location'] == reverse('evaluations:liste_repondant')


def test_creation_repondant_no_admin(client, formulaire_factory):

    form = formulaire_factory(
            type_form=Formulaire.SELECT_VAL,
            typegraphe=Formulaire.BARRE
    )

    response = client.post(
        reverse('evaluations:creation_repondant'),
        {
            'first_name': 'ham',
            'last_name': 'James',
            'email': 'hamady@hashbang.fr',
            'formulaires': [form.pk]
        }
    )
    assert response.status_code == 302

    assert reverse('evaluations:login') in response.url


def test_crea_repondant_veification_email(client, formulaire_factory,
                                          user_factory):

    form = formulaire_factory(
            type_form=Formulaire.SELECT_VAL,
            typegraphe=Formulaire.BARRE
    )
    user = user_factory(
        first_name="Ham",
        last_name="James",
        email="hamadybarry32@yahoo.fr"
    )

    response = client.post(
        reverse('evaluations:creation_repondant'),
        {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'formulaires': [form.pk]
        }
    )
    assert response.status_code == 302
    assert reverse('evaluations:login') in response.url
    assert user.email == user.email


def test_crea1_repondant_veification_email(admin_client, formulaire_factory,
                                           user_factory):

    form = formulaire_factory(
            type_form=Formulaire.SELECT_VAL,
            typegraphe=Formulaire.BARRE
    )
    user = user_factory(
        first_name="Ham",
        last_name="James",
        email="hamadybarry32@yahoo.fr"
    )

    response = admin_client.post(
        reverse('evaluations:creation_repondant'),
        {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'formulaires': [form.pk]
        }
    )
    assert response.status_code == 200


def test_edition_repondant_admin(admin_client, user_factory):
    user = user_factory(
        first_name="Ham",
        last_name="James",
        email="hamadybarry32@yahoo.fr"
    )
    response = admin_client.post(
        reverse('evaluations:edition_repondant', kwargs={'pk': user.pk}),
        {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
         }
      )
    assert response.status_code == 302
    assert response['Location'] == reverse('evaluations:liste_repondant')
    assert len(mail.outbox) == 0


def test_intro_formulaire_wrong_token(client):
    response = client.get(reverse(
        'evaluations:introduction_formulaire',
        kwargs={'token': str(uuid.uuid4())}
    ))

    assert response.status_code == 404


def test_generation_graphe(admin_client, formulaire_factory, categorie_factory,
                           question_factory, choice_factory,
                           choiceutilisateur_factory, user_factory):
    form = formulaire_factory(
        type_form=Formulaire.SELECT_VAL,
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
    response = admin_client.get(reverse(
        'evaluations:graphe',
        kwargs={
            'formulaire_pk': form.pk,
            'user_pk': user.pk
        }
    ))
    assert response.status_code == 200


def test_generation_graphe_g(admin_client, formulaire_factory,
                             categorie_factory, question_factory,
                             choice_factory, choiceutilisateur_factory,
                             user_factory):
    form = formulaire_factory(
        type_form=Formulaire.SELECT_VAL,
        typegraphe=Formulaire.BARRE
    )
    user = user_factory(
        first_name="Ham",
        last_name="James",
        email="hamadybarry32@yahoo.fr"
    )
    question = question_factory(
        question_text="test",
        formulaire=form
    )
    categorie1 = categorie_factory(
        categorie_text="test",
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
    response = admin_client.get(reverse(
        'evaluations:graphe_g',
        kwargs={
            'formulaire_pk': form.pk,
            'user_pk': user.pk
        }
    ))
    assert response.status_code == 200


def test_generation_graphe_s(admin_client, formulaire_factory,
                             categorie_factory, question_factory,
                             choice_factory, choiceutilisateur_factory,
                             user_factory):
    form = formulaire_factory(
        type_form=Formulaire.SELECT_VAL,
        typegraphe=Formulaire.BARRE
    )
    user = user_factory(
        first_name="Ham",
        last_name="James",
        email="hamadybarry32@yahoo.fr"
    )
    question = question_factory(
        question_text="test",
        formulaire=form
    )
    categorie1 = categorie_factory(
        categorie_text="test",
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
    categorie5 = categorie_factory(
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
    choice5 = choice_factory(
        choice_text="test",
        question=question,
        categorie=categorie5
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
    choiceutilisateur_factory(
        reference_user=user,
        reference_choice=choice5,
        valeur_entier=0
    )
    response = admin_client.get(reverse(
        'evaluations:graphe_s',
        kwargs={
            'formulaire_pk': form.pk,
            'user_pk': user.pk
        }
    ))
    assert response.status_code == 200


def test_liste_repondant_admin(admin_client, formulaire_factory):
    formulaire_factory(
        type_form=Formulaire.SELECT_VAL,
        typegraphe=Formulaire.BARRE
     )

    response = admin_client.get(reverse(
        'evaluations:liste_repondant'
    ))
    assert response.status_code == 200


def test_liste_repondant_no_admin(client):
    response = client.get(reverse(
        'evaluations:liste_repondant'
    ))
    assert response.status_code == 302
    assert reverse('evaluations:login') in response.url


def test_list2_formulaire_admin(admin_client, formulaire_factory):
    formulaire_factory(
        type_form=Formulaire.POND,
        typegraphe=Formulaire.BARRE
    )

    response = admin_client.get(reverse('evaluations:liste_formulaire'))

    assert response.status_code == 200

    assert response.context_data['nombre'] == 1


def test_list2_formulaire_no_admin(client, formulaire_factory):
    formulaire_factory(
        type_form=Formulaire.POND,
        typegraphe=Formulaire.BARRE
    )

    response = client.get(reverse('evaluations:liste_formulaire'))

    assert response.status_code == 302

    assert reverse('evaluations:login') in response.url


def test_create1_formulaire_admin(admin_client):

    assert Formulaire.objects.count() == 0

    response = admin_client.post(
        reverse('evaluations:creation_formulaire'),
        {
            'titre': 'titre',
            'introduction': 'intro',
            'type_form': Formulaire.SELECT_VAL,
            'typegraphe': Formulaire.BARRE,
            'nb_points': 10
        }
    )
    assert response.status_code == 302

    assert Formulaire.objects.count() == 1

    formulaire = Formulaire.objects.first()

    assert response['Location'] == reverse(
        'evaluations:formulaire',
        kwargs={'pk': formulaire.pk}
    )


def test_create1_formulaire_non_admin(client):

    assert Formulaire.objects.count() == 0

    response = client.post(
        reverse('evaluations:creation_formulaire'),
        {
            'titre': 'titre',
            'introduction': 'intro',
            'type_form': Formulaire.SELECT_VAL,
            'typegraphe': Formulaire.BARRE,
            'nb_points': 10
        }
    )
    assert response.status_code == 302

    assert reverse('evaluations:login') in response.url


def test_create2_formulaire_admin(admin_client):

    assert Formulaire.objects.count() == 0

    response = admin_client.post(
        reverse('evaluations:creation_formulaire'),
        {
            'titre': 'titre',
            'introduction': 'intro',
            'type_form': Formulaire.POND,
            'typegraphe': Formulaire.SELECT,
            'nb_points': 10
        }
    )
    assert response.status_code == 302

    assert Formulaire.objects.count() == 1

    formulaire = Formulaire.objects.first()

    assert response['Location'] == reverse(
        'evaluations:formulaire',
        kwargs={'pk': formulaire.pk}
    )


def test_create2_formulaire_no_admin(client):

    assert Formulaire.objects.count() == 0

    response = client.post(
        reverse('evaluations:creation_formulaire'),
        {
            'titre': 'titre',
            'introduction': 'intro',
            'type_form': Formulaire.POND,
            'typegraphe': Formulaire.SELECT,
            'nb_points': 10
        }
    )
    assert response.status_code == 302

    assert reverse('evaluations:login') in response.url


def test_edition_formulaire_admin(admin_client, formulaire_factory):

    form = formulaire_factory(
        type_form=Formulaire.SELECT_VAL,
        typegraphe=Formulaire.BARRE
    )

    response = admin_client.post(
        reverse('evaluations:edition_formulaire', kwargs={'pk': form.pk}),
        {
            'titre': form.titre,
            'introduction': form.introduction,
            'type_form': form.type_form,
            'typegraphe': form.typegraphe,
            'nb_points': form.nb_points
        }
    )
    assert response.status_code == 302

    assert response['Location'] == reverse(
        'evaluations:formulaire',
        kwargs={'pk': form.pk}
    )


def test_edition_formulaire_no_admin(client, formulaire_factory):

    form = formulaire_factory(
        type_form=Formulaire.SELECT_VAL,
        typegraphe=Formulaire.BARRE
    )

    response = client.post(
        reverse('evaluations:edition_formulaire', kwargs={'pk': form.pk}),
        {
            'titre': form.titre,
            'introduction': form.introduction,
            'type_form': form.type_form,
            'typegraphe': form.typegraphe,
            'nb_points': form.nb_points
        }
    )
    assert response.status_code == 302

    assert reverse('evaluations:login') in response.url


def test_edition1_formulaire_admin(admin_client, formulaire_factory):

    form = formulaire_factory(
        type_form=Formulaire.POND,
        typegraphe=Formulaire.SELECT
    )

    response = admin_client.post(
        reverse('evaluations:edition_formulaire', kwargs={'pk': form.pk}),
        {
            'titre': form.titre,
            'introduction': form.introduction,
            'type_form': form.type_form,
            'typegraphe': form.typegraphe,
            'nb_points': form.nb_points
        }
    )
    assert response.status_code == 302

    assert response['Location'] == reverse(
        'evaluations:formulaire',
        kwargs={'pk': form.pk}
    )


def test_edition1_formulaire_no_admin(client, formulaire_factory):

    form = formulaire_factory(
        type_form=Formulaire.POND,
        typegraphe=Formulaire.SELECT
    )

    response = client.post(
        reverse('evaluations:edition_formulaire', kwargs={'pk': form.pk}),
        {
            'titre': form.titre,
            'introduction': form.introduction,
            'type_form': form.type_form,
            'typegraphe': form.typegraphe,
            'nb_points': form.nb_points
        }
    )
    assert response.status_code == 302

    assert reverse('evaluations:login') in response.url


def test_create_question_admin(admin_client, formulaire_factory):

    form = formulaire_factory(
        type_form=Formulaire.POND,
        typegraphe=Formulaire.BARRE
    )

    response = admin_client.post(
        reverse(
            'evaluations:creation_question',
            kwargs={'formulaire_pk': form.pk}
        ), {'question_text': 'question_test'}
    )

    assert response.status_code == 302

    assert response['Location'] == reverse(
        'evaluations:formulaire',
        kwargs={'pk': form.pk}
    )


def test_create_question_no_admin(client, formulaire_factory):

    form = formulaire_factory(
        type_form=Formulaire.POND,
        typegraphe=Formulaire.BARRE
    )

    response = client.post(
        reverse(
            'evaluations:creation_question',
            kwargs={'formulaire_pk': form.pk}
        ), {'question_text': 'question_test'}
    )

    assert response.status_code == 302

    assert reverse('evaluations:login') in response.url


def test_edition_question_admin(admin_client, formulaire_factory,
                                question_factory):
    form = formulaire_factory(
        type_form=Formulaire.POND,
        typegraphe=Formulaire.BARRE
    )
    question = question_factory(formulaire=form)
    url = reverse(
        'evaluations:edition_question',
        kwargs={'formulaire_pk': form.pk, 'pk': question.pk}
    )
    response = admin_client.post(
        url, {'question_text': question.question_text, 'formulaire': form.pk}
    )
    assert response.status_code == 302

    assert response['Location'] == reverse(
        'evaluations:formulaire',
        kwargs={'pk': form.pk}
    )


def test_edition_question_no_admin(client, formulaire_factory,
                                   question_factory):
    form = formulaire_factory(
        type_form=Formulaire.POND,
        typegraphe=Formulaire.BARRE
    )
    question = question_factory(formulaire=form)

    url = reverse(
        'evaluations:edition_question',
        kwargs={'formulaire_pk': form.pk, 'pk': question.pk}
    )
    response = client.post(
        url,
        {
            'question_text': question.question_text,
            'formulaire': form.pk
        }
    )
    assert response.status_code == 302

    assert reverse('evaluations:login') in response.url


def test_create_categorie_admin(admin_client, formulaire_factory):

    form = formulaire_factory(
        type_form=Formulaire.POND,
        typegraphe=Formulaire.BARRE
    )

    response = admin_client.post(
        reverse(
            'evaluations:creation_categorie',
            kwargs={'formulaire_pk': form.pk}
        ), {'categorie_text': 'categorie_test'}
    )

    assert response.status_code == 302

    assert response['Location'] == reverse(
        'evaluations:formulaire',
        kwargs={'pk': form.pk}
    )


def test_create_categorie_no_admin(client, formulaire_factory):

    form = formulaire_factory(
        type_form=Formulaire.POND,
        typegraphe=Formulaire.BARRE
    )

    response = client.post(
        reverse(
            'evaluations:creation_categorie',
            kwargs={'formulaire_pk': form.pk}
        ), {'categorie_text': 'categorie_test'}
    )

    assert response.status_code == 302

    assert reverse('evaluations:login') in response.url


def test_edition_categorie_admin(admin_client, formulaire_factory,
                                 categorie_factory):
    form = formulaire_factory()
    categorie = categorie_factory(formulaire=form)

    url = reverse(
        'evaluations:edition_categorie',
        kwargs={'formulaire_pk': form.pk, 'pk': categorie.pk}
    )
    response = admin_client.post(
        url,
        {'categorie_text': categorie.categorie_text, 'formulaire': form.pk}
    )

    assert response.status_code == 302

    assert response['Location'] == reverse(
        'evaluations:formulaire',
        kwargs={'pk': form.pk}
    )


def test_edition_categorie_no_admin(client, formulaire_factory,
                                    categorie_factory):
    form = formulaire_factory()
    categorie = categorie_factory(formulaire=form)
    url = reverse(
        'evaluations:edition_categorie',
        kwargs={'pk': categorie.pk, 'formulaire_pk': form.pk}
    )
    response = client.post(
        url,
        {'categorie_text': categorie.categorie_text, 'formulaire': form.pk}
    )

    assert response.status_code == 302

    assert reverse('evaluations:login') in response.url


def test_create_choice_admin(admin_client, question_factory,
                             categorie_factory):

    question = question_factory()
    categorie = categorie_factory(formulaire=question.formulaire)

    response = admin_client.post(
        reverse(
            'evaluations:creation_choice',
            kwargs={
                'formulaire_pk': question.formulaire.pk,
                'question_pk': question.pk
            }
        ), {
            'choice_text': 'choice_text',
            'categorie': categorie.pk,
            'question': question.pk,
            'valorisation': Choice.VALPLUS0
        }
    )
    assert response.status_code == 302

    assert response['Location'] == reverse(
        'evaluations:formulaire',
        kwargs={'pk': question.formulaire.pk}
    )


def test_create_choice_no_admin(client, question_factory,
                                categorie_factory):

    question = question_factory()
    categorie = categorie_factory(formulaire=question.formulaire)

    response = client.post(
        reverse(
            'evaluations:creation_choice',
            kwargs={
                'formulaire_pk': question.formulaire.pk,
                'question_pk': question.pk
            }
        ), {
            'choice_text': 'choice_text',
            'categorie': categorie.pk,
            'question': question.pk,
            'valorisation': Choice.VALPLUS0
        }
    )
    assert response.status_code == 302

    assert reverse('evaluations:login') in response.url


def test_edition_choice_admin(admin_client, formulaire_factory,
                              question_factory, categorie_factory,
                              choice_factory):

    form = formulaire_factory()
    question = question_factory(formulaire=form)
    categorie = categorie_factory(formulaire=form)
    choice = choice_factory(valorisation='+1', question=question)

    url = reverse(
        'evaluations:edition_choice', kwargs={
            'formulaire_pk': form.pk,
            'question_pk': question.pk,
            'choice_pk': choice.pk
        }
    )

    response = admin_client.post(
        url,
        {
            'choice_text': choice.choice_text,
            'question': question.pk,
            'categorie': categorie.pk,
            'valorisation': choice.valorisation
        }
    )
    assert response.status_code == 302

    assert response['Location'] == reverse(
        'evaluations:formulaire',
        kwargs={'pk': form.pk}
    )


def test_edition_choice_no_admin(client, formulaire_factory,
                                 question_factory, categorie_factory,
                                 choice_factory):

    form = formulaire_factory()
    question = question_factory(formulaire=form)
    categorie = categorie_factory(formulaire=form)
    choice = choice_factory(valorisation='+1', question=question)

    url = reverse(
        'evaluations:edition_choice', kwargs={
            'formulaire_pk': question.formulaire.pk,
            'question_pk': question.pk,
            'choice_pk': choice.pk,
        }
    )

    response = client.post(
        url,
        {
            'choice_text': choice.choice_text,
            'question': question.pk,
            'categorie': categorie.pk,
            'valorisation': choice.valorisation
        }
    )
    assert response.status_code == 302

    assert reverse('evaluations:login') in response.url


def test_get_context_question_admin(admin_client, formulaire_factory,
                                    question_factory):
    form = formulaire_factory()
    question = question_factory(formulaire=form)

    response = admin_client.get(
        reverse(
            'evaluations:creation_question', kwargs={'formulaire_pk': form.pk}
        ), {'question_text': question.question_text, 'formulaire': form.pk}
    )

    assert response.status_code == 200


def test_get_context_question_no_admin(client, formulaire_factory,
                                       question_factory):
    form = formulaire_factory()
    question = question_factory(formulaire=form)

    response = client.get(
        reverse(
            'evaluations:creation_question', kwargs={'formulaire_pk': form.pk}
        ), {'question_text': question.question_text, 'formulaire': form.pk}
    )

    assert response.status_code == 302


def test_get_context_categorie_admin(admin_client, formulaire_factory,
                                     categorie_factory):
    form = formulaire_factory()
    categorie = categorie_factory(formulaire=form)

    response = admin_client.get(
        reverse(
            'evaluations:creation_categorie', kwargs={'formulaire_pk': form.pk}
        ), {'categorie_text': categorie.categorie_text, 'formulaire': form.pk}
    )

    assert response.status_code == 200


def test_get_context_categorie_no_admin(client, formulaire_factory,
                                        categorie_factory):
    form = formulaire_factory()
    categorie = categorie_factory(formulaire=form)

    response = client.get(
        reverse(
            'evaluations:creation_categorie', kwargs={'formulaire_pk': form.pk}
        ), {'categorie_text': categorie.categorie_text, 'formulaire': form.pk}
    )

    assert response.status_code == 302


def test_get_context_choice_admin(admin_client, question_factory,
                                  categorie_factory, choice_factory):
    question = question_factory()
    categorie = categorie_factory(formulaire=question.formulaire)
    choix = choice_factory(question=question)

    response = admin_client.get(
        reverse(
            'evaluations:creation_choice',
            kwargs={
                'formulaire_pk': question.formulaire.pk,
                'question_pk': question.pk
            }
        ), {
            'choice_text': choix.choice_text,
            'question': question.pk,
            'categorie': categorie.pk,
            'valorisation': choix.valorisation
        }
    )

    assert response.status_code == 200


def test_get_context_choice_no_admin(client, question_factory,
                                     categorie_factory, choice_factory):
    question = question_factory()
    categorie = categorie_factory(formulaire=question.formulaire)
    choix = choice_factory(question=question)

    response = client.get(
        reverse(
            'evaluations:creation_choice',
            kwargs={
                'formulaire_pk': question.formulaire.pk,
                'question_pk': question.pk
            }
        ), {
            'choice_text': choix.choice_text,
            'question': question.pk,
            'categorie': categorie.pk,
            'valorisation': choix.valorisation
        }
    )

    assert response.status_code == 302


def test_repondre_question_admin(admin_client, formulaire_factory,
                                 question_factory, user_factory,
                                 ticket_factory, choiceutilisateur_factory,
                                 choice_factory, categorie_factory):
    form = formulaire_factory(
        type_form=Formulaire.POND,
        typegraphe=Formulaire.BARRE
    )
    user_factory(
        first_name="Ham",
        last_name="James",
        email="hamadybarry32@yahoo.fr"
    )
    question = question_factory(formulaire=form)

    categorie = categorie_factory(
        categorie_text="test",
        formulaire=form
    )
    categorie1 = categorie_factory(
        categorie_text="test",
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
    choice = choice_factory(
        choice_text="test",
        question=question,
        categorie=categorie
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

    response = admin_client.post(
        reverse(
            'evaluations:repondre_question',
            kwargs={'formulaire_pk': form.pk, 'question_pk': question.pk}
        ),
        {choice.pk: 10, choice1.pk: 0, choice2.pk: 0, choice3.pk: 0},
    )

    assert response.status_code == 302
    assert response['Location'] == reverse('evaluations:conclusion')
    assert len(mail.outbox) == 1


def test_repondre_question_no_admin(client, formulaire_factory,
                                    question_factory):
    form = formulaire_factory(
        type_form=Formulaire.POND,
        typegraphe=Formulaire.BARRE
    )
    question = question_factory(formulaire=form)

    response = client.get(
        reverse(
            'evaluations:repondre_question',
            kwargs={'formulaire_pk': form.pk, 'question_pk': question.pk}
        )
    )

    assert response.status_code == 302


def test_repondre1_question_admin(admin_client, formulaire_factory,
                                  question_factory):
    form = formulaire_factory(
        type_form=Formulaire.SELECT_VAL,
        typegraphe=Formulaire.BARRE
    )
    question = question_factory(formulaire=form)

    response = admin_client.get(
        reverse(
            'evaluations:repondre_question',
            kwargs={'formulaire_pk': form.pk, 'question_pk': question.pk}
        )
    )

    assert response.status_code == 200


def test_repondre1_question_no_admin(client, formulaire_factory,
                                     question_factory):
    form = formulaire_factory(
        type_form=Formulaire.SELECT_VAL,
        typegraphe=Formulaire.BARRE
    )
    question = question_factory(formulaire=form)

    response = client.get(
        reverse(
            'evaluations:repondre_question',
            kwargs={'formulaire_pk': form.pk, 'question_pk': question.pk}
        )
    )

    assert response.status_code == 302


def test_creation_pdf_admin(admin_client, formulaire_factory, user_factory,
                            question_factory, categorie_factory,
                            choice_factory, choiceutilisateur_factory):
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
            'evaluations:creation_pdf',
            kwargs={'formulaire_pk': form.pk, 'user_pk': user.pk}
        )
    )

    assert response.status_code == 200


def test_creation_pdf_no_admin(client, formulaire_factory, user_factory):
    form = formulaire_factory(
        type_form=Formulaire.POND,
        typegraphe=Formulaire.BARRE
    )
    user = user_factory(
        first_name="Ham",
        last_name="James",
        email="hamadybarry32@yahoo.fr"
    )
    response = client.get(
        reverse(
            'evaluations:creation_pdf',
            kwargs={'formulaire_pk': form.pk, 'user_pk': user.pk}
        )
    )

    assert response.status_code == 302


def test_conclusion_admin(admin_client):
    response = admin_client.get(
        reverse('evaluations:conclusion')
    )
    assert response.status_code == 200


def test_conclusion_no_admin(client):
    response = client.get(
        reverse('evaluations:conclusion')
    )
    assert response.status_code == 302
    assert reverse('evaluations:login') in response.url


def test_create_choiceuser_admin(admin_client, formulaire_factory,
                                 question_factory, choice_factory):

    form = formulaire_factory(
        type_form=Formulaire.POND,
        typegraphe=Formulaire.BARRE,
        nb_points=10
    )
    question = question_factory(formulaire=form)
    choice = choice_factory(question=question)
    choice2 = choice_factory(question=question)
    choice3 = choice_factory(question=question)
    choice4 = choice_factory(question=question)

    assert ChoiceUtilisateur.objects.count() == 0

    response = admin_client.post(
        reverse(
            'evaluations:repondre_question',
            kwargs={'formulaire_pk': form.pk, 'question_pk': question.pk}
        ),
        {
            str(choice.pk): 6,
            str(choice2.pk): 4,
            str(choice3.pk): 7,
            str(choice4.pk): 5,
        }
    )
    assert response.status_code == 200


def test_create1_choiceuser(admin_client, formulaire_factory,
                            question_factory, choice_factory):

    form = formulaire_factory(
        type_form=Formulaire.POND,
        typegraphe=Formulaire.BARRE,
        nb_points=20
    )
    question = question_factory(formulaire=form)
    choice = choice_factory(question=question)
    choice2 = choice_factory(question=question)

    assert ChoiceUtilisateur.objects.count() == 0

    response = admin_client.post(
        reverse(
            'evaluations:repondre_question',
            kwargs={'formulaire_pk': form.pk, 'question_pk': question.pk}
        ),
        {
            str(choice.pk): 6,
            str(choice2.pk): 6
        }
    )
    assert response.status_code == 200


def test_create_choiceuser_no_admin(client, formulaire_factory,
                                    question_factory, choice_factory):

    form = formulaire_factory(
        type_form=Formulaire.POND,
        typegraphe=Formulaire.BARRE,
        nb_points=10
    )
    question = question_factory(formulaire=form)
    choice = choice_factory(question=question)
    choice2 = choice_factory(question=question)

    assert ChoiceUtilisateur.objects.count() == 0

    response = client.post(
        reverse(
            'evaluations:repondre_question',
            kwargs={'formulaire_pk': form.pk, 'question_pk': question.pk}
        ),
        {
            str(choice.pk): 6,
            str(choice2.pk): 4
        }
    )
    assert response.status_code == 302

    assert reverse('evaluations:login') in response.url


def test_create1_choiceuser_admin(admin_client, formulaire_factory,
                                  question_factory, choice_factory):

    form = formulaire_factory(
        type_form=Formulaire.POND,
        typegraphe=Formulaire.BARRE,
        nb_points=10
    )

    question = question_factory(formulaire=form)
    quest = question_factory(formulaire=form)

    choice = choice_factory(question=question)
    choice2 = choice_factory(question=question)

    assert ChoiceUtilisateur.objects.count() == 0

    response = admin_client.post(
        reverse(
            'evaluations:repondre_question',
            kwargs={'formulaire_pk': form.pk, 'question_pk': question.pk}
        ),
        {
            str(choice.pk): 3,
            str(choice2.pk): 7
        }
    )
    assert response.status_code == 302

    assert ChoiceUtilisateur.objects.count() == 2

    assert response['Location'] == reverse(
        'evaluations:repondre_question',
        kwargs={'formulaire_pk': form.pk, 'question_pk': quest.pk}
    )


def test_create1_choiceuser_no_admin(client, formulaire_factory,
                                     question_factory, choice_factory):

    form = formulaire_factory(
        type_form=Formulaire.POND,
        typegraphe=Formulaire.BARRE,
        nb_points=10
    )

    question = question_factory(formulaire=form)

    choice = choice_factory(question=question)
    choice2 = choice_factory(question=question)

    assert ChoiceUtilisateur.objects.count() == 0

    response = client.post(
        reverse(
            'evaluations:repondre_question',
            kwargs={'formulaire_pk': form.pk, 'question_pk': question.pk}
        ),
        {
            str(choice.pk): 3,
            str(choice2.pk): 7
        }
    )
    assert response.status_code == 302

    assert reverse('evaluations:login') in response.url


def test_select_formulaire_admin(admin_client, formulaire_factory,
                                 question_factory, choice_factory):

    form = formulaire_factory(
        type_form=Formulaire.SELECT,
        typegraphe=Formulaire.SELECT,
        nb_points=0
    )

    question = question_factory(formulaire=form)

    choice = choice_factory(question=question)
    response = admin_client.post(
        reverse(
            'evaluations:repondre_question',
            kwargs={'formulaire_pk': form.pk, 'question_pk': question.pk}
        ),
        {
            str(choice.pk): choice
        }
    )
    assert response.status_code == 200


def test_select_formulaire_no_admin(client, formulaire_factory,
                                    question_factory, choice_factory):

    form = formulaire_factory(
        type_form=Formulaire.SELECT,
        typegraphe=Formulaire.SELECT,
        nb_points=0
    )

    question = question_factory(formulaire=form)

    choice = choice_factory(question=question)

    response = client.post(
        reverse(
            'evaluations:repondre_question',
            kwargs={'formulaire_pk': form.pk, 'question_pk': question.pk}
        ),
        {
            str(choice.pk): choice.pk
        }
    )
    assert response.status_code == 302

    assert reverse('evaluations:login') in response.url


def test_formulaire_detail(admin_client, formulaire, question_factory,
                           choice_factory, categorie_factory):
    question = question_factory(formulaire=formulaire)
    categorie = categorie_factory(formulaire=formulaire)
    choice_factory(question=question, categorie=categorie)

    url = reverse('evaluations:formulaire', kwargs={'pk': formulaire.pk})
    response = admin_client.get(url)
    assert response.status_code == 200
