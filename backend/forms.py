from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email address is already registered.")
        return email
