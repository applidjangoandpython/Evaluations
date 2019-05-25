from django.conf.urls import url
from .views_eval import (
    Accueil,
    TokenEntryPoint,
    Repondre_Question,
    Conclusion,
)

urlpatterns = [
    url(
        r'^$',
        Accueil.as_view(),
        name='accueil'
    ),

    url(
        r'^token/(?P<token>.*)/$',
        TokenEntryPoint.as_view(),
        name='introduction_formulaire'
    ),

    url(
        r'^formulaires/(?P<formulaire_pk>[0-9]+)/questions/'
        '(?P<question_pk>[0-9]+)/$',
        Repondre_Question.as_view(),
        name='repondre_question'
    ),

    url(
        r'^conclusion/$',
        Conclusion.as_view(),
        name='conclusion'
    ),
]
