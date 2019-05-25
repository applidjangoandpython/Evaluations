from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)


urlpatterns = [
    path(
        'login/',
        LoginView.as_view(template_name='evaluations/login.html'),
        name='login'
    ),

    path(
        'logout/',
        LogoutView.as_view(next_page='evaluations:home'),
        name='logout'
    ),
    path(
        'password_reset/',
        PasswordResetView.as_view(
            template_name='evaluations/password_reset_form.html',
            success_url=reverse_lazy('evaluations:password_reset_done'),
            email_template_name='evaluations/password_reset_email.html',
        ),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(
            template_name='evaluations/password_reset_done.html',
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='evaluations/password_reset_confirm.html',
            success_url=reverse_lazy('evaluations:password_reset_complete'),
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        PasswordResetCompleteView.as_view(
            template_name='evaluations/password_reset_complete.html',
        ),
        name='password_reset_complete'
    ),
]
