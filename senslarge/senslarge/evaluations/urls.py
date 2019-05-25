from django.conf.urls import include, url

from .views_eval import Root

app_name = 'evaluations'

urlpatterns = [
    url(r'^gestion/', include('senslarge.evaluations.urls_mgmt')),
    url(r'^evaluation/', include('senslarge.evaluations.urls_eval')),
    url(r'^auth/', include('senslarge.evaluations.urls_auth')),
    url(r'^$', Root.as_view(), name='root'),
]
