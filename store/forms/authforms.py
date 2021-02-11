from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm


class CustomerAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", required=True)


class CustomerCreationForm(UserCreationForm):
    username = forms.EmailField(label="Email", required=True)
    first_name = forms.CharField(label="Name", required=True)

    def clean_first_name(self):
        data = self.cleaned_data.get("first_name")
        if len(data.strip()) < 4:
            raise ValidationError("First Name must be 4 char long")
        return data.strip()

    class Meta:
        model = User  # import User from auth
        fields = ['username', 'first_name']


