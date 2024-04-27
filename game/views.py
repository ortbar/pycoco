from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import RegisterForm, LoginForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def base(request):
    return render(request, "base.html")

# Create your views here.
def hello(request):
    return render(request, "hello.html")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            email = form.cleaned_data.get("email")
            User.objects.create_user(username=username, password=password, email=email)
            return redirect("hello")  # Redirige al usuario a la página de inicio de sesión después del registro
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

def logout(request):
    logout(request)
    return redirect("base")

def estadisticas(request):
    return render(request, "estadisticas.html") 

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("profile")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

def game (request):
    return render(request, "game.html")



            
        
            


