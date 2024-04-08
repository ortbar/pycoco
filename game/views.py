from django.shortcuts import render
from django.http import HttpResponse
from .forms import RegisterForm, LoginForm

def index(request):
    return HttpResponse("Hello, world. You're at the game index.")

# Create your views here.
def hello(request):
    return render(request, "hello.html")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        print(form)
        if form.is_valid():
            email = request.POST.get("email")
            password = request.POST.get("password")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            username = request.POST.get("username")
            
            
            # Aquí deberíamos guardar el usuario en la base de datos:
            
         

            
    else:
        form = RegisterForm()
    return render(request, "register.html")

