from django import forms

# tenemos que crear una clase que herede de forms.Form, y definir los campos que queremos que tenga, por ejemplo, para login:
class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    # definimos los campos que queremos que tenga el formulario
    email = forms.EmailField(label="email")
    password = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="repeat_password", widget=forms.PasswordInput)
    first_name = forms.CharField(label="first_name")
    last_name = forms.CharField(label="last_name")
    username = forms.CharField(label="username")
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
    
    

