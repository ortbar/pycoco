from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from django.contrib.auth.models import User
# importar ésto para el proceso de user-signup ya que es más sencillo
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate
from .models import userProfile


# tenemos que crear una clase que herede de forms.Form, y definir los campos que queremos que tenga, por ejemplo, para login:
# class LoginForm(forms.Form):

class LoginForm(forms.Form):
    email = forms.EmailField(label="username", required=True)
    password = forms.CharField(label="password", widget=forms.PasswordInput)

    
    # SignUpForm: Hereda de UserCreationForm, una clase de formulario integrada en Django específicamente diseñada para la creación de usuarios.
#  RegisterForm: Hereda directamente de forms.Form y define campos y validaciones personalizados.
#  SignUpForm es la clase que usa la herramienta de registro que ya trae Django (UserCreationForm). Esto hace que sea más fácil de mantener y menos propensa a errores, ya que aprovecha las validaciones y la lógica de creación de usuarios integradas en Django.

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

# class RegisterForm(forms.Form):
#     alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
#     email = forms.EmailField(label="email", required=True)
#     password = forms.CharField(label="password", widget=forms.PasswordInput, min_length=6, validators=[alphanumeric])
#     password2 = forms.CharField(label="password2", widget=forms.PasswordInput, min_length=6, validators=[alphanumeric])
#     first_name = forms.CharField(label="first_name", min_length=6, validators=[alphanumeric])
#     username = forms.CharField(label="username", min_length=6, validators=[alphanumeric])

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if User.objects.filter(email=email).exists():
#             raise ValidationError("Email already exists")
#         return email

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         password2 = cleaned_data.get("password2")
#         if password != password2:
#             raise forms.ValidationError("Passwords do not match")
#         return cleaned_data
    
class UserProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)

    class Meta:
        model = userProfile
        fields = ['avatar']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].initial = self.instance.user.username

    def save(self, commit=True):
        user_profile = super(UserProfileForm, self).save(commit=False)
        user_profile.user.username = self.cleaned_data['username']
        if commit:
            user_profile.user.save()
            user_profile.save()
        return user_profile




