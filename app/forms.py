from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UsernameField,
)
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Customer, LostItem


class CustomerRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["username", "email"]
        labels = {"email": "Email"}
        widgets = {"username": forms.TextInput(attrs={"class": "form-control"})}

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A User with this email already exists.")
        return email


class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control"})
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "class": "form-control"}
        ),
    )


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name"]
        widgets = {"name": forms.TextInput(attrs={"class": "form-control"})}


class EmailForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)


class ImageUploadForm(forms.ModelForm):
    image = forms.FileField(
        widget=forms.TextInput(
            attrs={
                "name": "images",
                "type": "File",
                "class": "form-control",
                "multiple": "True",
            }
        ),
        label="",
    )

    class Meta:
        model = LostItem
        fields = ["image"]
