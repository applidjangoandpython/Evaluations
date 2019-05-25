from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^_ht/', include('django_healthchecks.urls')),
    url(r'^', include('senslarge.evaluations.urls')),
]
