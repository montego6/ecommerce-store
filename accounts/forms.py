from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, help_text='Ваше имя')
    email = forms.EmailField(max_length=254, help_text='Адрес вашей электронной почты')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2',)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)