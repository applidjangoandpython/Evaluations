
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from braces.views import SuperuserRequiredMixin


class LoginRequired(LoginRequiredMixin):
    login_url = reverse_lazy('evaluations:login')


class SuperuserRequired(SuperuserRequiredMixin):
    login_url = reverse_lazy('evaluations:login')
