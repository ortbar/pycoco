from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from django.contrib.auth.models import User


# tenemos que crear una clase que herede de forms.Form, y definir los campos que queremos que tenga, por ejemplo, para login:
class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    email = forms.EmailField(label="email", required=True)
    password = forms.CharField(label="password", widget=forms.PasswordInput, min_length=6, validators=[alphanumeric])
    password2 = forms.CharField(label="password2", widget=forms.PasswordInput, min_length=6, validators=[alphanumeric])
    first_name = forms.CharField(label="first_name", min_length=6, validators=[alphanumeric])
    last_name = forms.CharField(label="last_name", min_length=6, validators=[alphanumeric])
    username = forms.CharField(label="username", min_length=6, validators=[alphanumeric])

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
    
    

