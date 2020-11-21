from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
from .models import UserProfile


class SignUpForm(UserCreationForm):
    # username = UsernameField(
    #     label="Nazwa użytkownika",
    #     widget=forms.TextInput(
    #         attrs={'autofocus': True,
    #                'class': 'form-control-lg pr-4 shadow-none',
    #                'placeholder': 'Nazwa uzytkownika'},
    #     ),
    # )
    # email = forms.EmailField(
    #     max_length=254, label='Email',
    #     widget=forms.EmailInput(
    #         attrs={'class': 'form-control-lg pr-4 shadow-none'}),
    #     validators=[EmailValidator]
    # )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('city', 'phone_number', 'avatar')  # Note that we didn't mention user field here.

    def save(self, user=None):
        user_profile = super(UserProfileEditForm, self).save(commit=False)
        if user:
            user_profile.user = user
        user_profile.save()
        return user_profile


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
