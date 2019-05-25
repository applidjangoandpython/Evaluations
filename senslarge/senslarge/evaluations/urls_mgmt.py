from django.conf.urls import url
from .views_mgmt import (
    Home,
    Liste_Formulaire,
    Detail_Formulaire,
    Creation_Formulaire,
    Edition_Formulaire,
    Creation_Question,
    Edition_Question,
    Creation_Choices,
    Edition_Choices,
    Creation_Categories,
    Edition_Categories,
    Liste_Repondant,
    Creation_Repondant,
    Edition_Repondant,
    Detail_Repondant,
    Creation_PDF,
    GrapheView,
    GrapheView2,
    GrapheView3,
)

urlpatterns = [
    url(
        r'^$',
        Home.as_view(),
        name='home'
    ),

    url(
        r'^formulaires/$',
        Liste_Formulaire.as_view(),
        name='liste_formulaire'
    ),

    url(
        r'^formulaires/(?P<pk>[0-9]+)/$',
        Detail_Formulaire.as_view(),
        name='formulaire'
    ),

    url(
        r'^formulaires/creation/$',
        Creation_Formulaire.as_view(),
        name='creation_formulaire'
    ),

    url(
        r'^formulaires/(?P<pk>[0-9]+)/edition/$',
        Edition_Formulaire.as_view(),
        name='edition_formulaire'
    ),

    url(
        r'^formulaires/(?P<formulaire_pk>[0-9]+)/questions/creation/$',
        Creation_Question.as_view(),
        name='creation_question'
    ),

    url(
        r'^formulaires/(?P<formulaire_pk>[0-9]+)/questions/(?P<pk>[0-9]+)/$',
        Edition_Question.as_view(),
        name='edition_question'
    ),

    url(
        r'^formulaires/(?P<formulaire_pk>[0-9]+)/questions/'
        '(?P<question_pk>[0-9]+)/choix/creation/$',
        Creation_Choices.as_view(),
        name='creation_choice'
    ),

    url(
        r'^formulaires/(?P<formulaire_pk>[0-9]+)/questions/'
        '(?P<question_pk>[0-9]+)/choix/(?P<choice_pk>[0-9]+)/$',
        Edition_Choices.as_view(),
        name='edition_choice'
    ),

    url(
        r'^formulaires/(?P<formulaire_pk>[0-9]+)/categories/creation/$',
        Creation_Categories.as_view(),
        name='creation_categorie'
    ),
    url(
        r'^formulaires/(?P<formulaire_pk>[0-9]+)/categories/(?P<pk>[0-9]+)/$',
        Edition_Categories.as_view(),
        name='edition_categorie'
    ),

    url(
        r'^repondants/$',
        Liste_Repondant.as_view(),
        name='liste_repondant'
    ),

    url(
        r'^repondants/creation/$',
        Creation_Repondant.as_view(),
        name='creation_repondant'
    ),

    url(
        r'^repondants/(?P<pk>[0-9]+)/$',
        Edition_Repondant.as_view(),
        name='edition_repondant'
    ),
    url(
        r'^repondants/(?P<user_pk>[0-9]+)/formulaire/(?P<formulaire_pk>[0-9]+)'
        '/$',
        Detail_Repondant.as_view(),
        name='repondant'
    ),

    url(
        r'^repondants/(?P<user_pk>[0-9]+)/formulaire/(?P<formulaire_pk>[0-9]+)'
        '/pdf/$',
        Creation_PDF.as_view(),
        name='creation_pdf'
    ),

    url(
        r'^repondants/(?P<user_pk>[0-9]+)/formulaire/(?P<formulaire_pk>[0-9]+)'
        '/graphe/$',
        GrapheView.as_view(),
        name='graphe'
    ),

    url(
        r'^repondants/(?P<user_pk>[0-9]+)/formulaire/(?P<formulaire_pk>[0-9]+)'
        '/graphe_g/$',
        GrapheView2.as_view(),
        name='graphe_g'
    ),

    url(
        r'^repondants/(?P<user_pk>[0-9]+)/formulaire/(?P<formulaire_pk>[0-9]+)'
        '/graphe_s/$',
        GrapheView3.as_view(),
        name='graphe_s'
    ),
]
