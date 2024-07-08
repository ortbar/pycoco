from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from game.models import userProfile
from django.contrib.auth.decorators import login_required


from django.shortcuts import redirect
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from game.forms import UserProfileForm 







def base(request):
    return render(request, "index.html")

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("index")
        else:
            print("Formulario inválido")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            rawp_password = form.cleaned_data.get("password1")
            user = authenticate(username=username,password=rawp_password)
            if user is not None:
                auth_login(request,user)
                return redirect("login")
           # Redirige al usuario a la página de inicio de sesión después del registro
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

@login_required
def estadisticas(request):
    return render(request, "estadisticas.html") 



def logout(request):
        auth_logout(request)
        return redirect("/")

@login_required   
def game(request):
    return render(request, "game.html")

@login_required
def index(request):
    return render(request, "index.html")


# para proteger la vista de perfil, se utiliza el decorador login_required, 
# que redirige al usuario a la página de inicio de sesión si intenta acceder a la vista de perfil sin haber iniciado sesión.

@login_required
def profile(request, *args, **kwargs):
    user = request.user
    profile, created = userProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = UserProfileForm(instance=profile)

    return render(request, "profile.html", {"form": form})







            
        
            


