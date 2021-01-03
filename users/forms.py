from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
from .models import UserProfile


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserProfileEditForm(forms.ModelForm):
    phone_number = forms.CharField()
    city = forms.CharField()

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'city', 'avatar']  # Note that we didn't mention user field here.


class UserEditForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()


    class Meta:
        model = User
        fields = ['first_name', 'last_name']

