from . import models

from django import forms
from django.contrib.auth.models import User

MIN_LENGTH_PASSWORD = 3
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=MIN_LENGTH_PASSWORD, widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=255)
    email = forms.EmailField()
    password = forms.CharField(min_length=MIN_LENGTH_PASSWORD, widget=forms.PasswordInput)
    password_check = forms.CharField(min_length=MIN_LENGTH_PASSWORD, widget=forms.PasswordInput)

    class Meta:
        model = models.MyUser
        fields = ['avatar']

    def clean(self):
        password  = self.cleaned_data.get('password')
        password_check = self.cleaned_data.get('password_check')
        if password_check != password:
            raise forms.ValidationError("Password doesn't match")

        return self.cleaned_data

    def clean_username(self):
        print(self.cleaned_data.get('username'))
        print(models.MyUser.objects.filter(profile__username=self.cleaned_data.get('username')).exists())
        if models.MyUser.objects.filter(profile__username=self.cleaned_data.get('username')).exists():
            raise forms.ValidationError("User with same username exist")

        return self.username
    def save(self):
        profile = User.objects.create_user(username=self.cleaned_data.get('username'), email=self.cleaned_data.get('email'), password=self.cleaned_data.get('password'))
        return models.MyUser.objects.create(profile=profile, avatar=self.cleaned_data.get('avatar'))
