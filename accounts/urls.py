from django.contrib.auth.views import PasswordChangeView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path
from . import views

urlpatterns = [
    path("signup", views.signup, name="signup"),
    path("login", views.user_login, name="login"),
    path("logout", views.user_logout, name="logout"),
    path("change-password",
         PasswordChangeView.as_view(template_name="form.html", title="Смена пароля"),
         name="change-password"),
    path("reset-password",
         PasswordResetView.as_view(template_name="form.html",
                                   subject_template_name="registration/reset_subject.txt",
                                   email_template_name="registration/reset_email.txt"),
         name="password_reset"),
    path("reset-password/sent",
         PasswordResetDoneView.as_view(template_name="message.html",
                                       extra_context={"message": "Запрос успешно отправлен"}),
         name="password_reset_done"),
    path("reset-password/<uidb64>/<token>",
         PasswordResetConfirmView.as_view(template_name="form.html"), name="password_reset_confirm"),
    path("reset-password/done", PasswordResetCompleteView.as_view(template_name="message.html",
                                                                  extra_context={"message": "Пароль успешно изменен"}),
         name="password_reset_complete")
]