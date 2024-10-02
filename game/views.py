from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from game.models import userProfile
from django.contrib.auth.decorators import login_required


from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Game, Riddle, Match
from django.views.decorators.csrf import csrf_exempt
import json

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from game.forms import UserProfileForm 
from django.http import JsonResponse







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
def game(request, game_id):
    user = request.user
    # crear match (y guardarlo en la base de datos) y pasarlo por el return para saber el id e ir actualizando los puntos
    # y empezar con la lista de indices de los acertijos
    game = get_object_or_404(Game, id= game_id)

    # Verificar si ya existe un match para este usuario y juego
    match, created = Match.objects.get_or_create(user=user, game=game)
        # Si el match es nuevo, se inicializa los puntos y la lista de acertijos vistos
    if created:
        match.points = 0  # Inicializamos los puntos en cero
        match.acertijos_vistos = []  # Creamos una lista vacía para los acertijos vistos
        match.save()  # Guardamos el nuevo match en la base de datos

        # filtrar acertijos que no se han visto
        riddles = Riddle.objects.filter(game=game).exclude(id__in=match.acertijos_vistos)

        # Si el usuario resuelve un acertijo correctamente, añadirlo a seen_riddles
        if request.method == "POST":
            riddle_id = int(request.POST.get('riddle_id'))
            if riddle_id not in match.seen_riddles:
                match.acertijos_vistos(riddle_id)  # Añadimos el ID del acertijo visto
                match.save()  # Guardamos el Match actualizado en la base de datos

        context = {
        'match': match,
        'game': game,
        'riddles': riddles,
        }
        
        return render(request, "game.html")

## crear un metodo que sea para el boton de next que le pases el id del match actual
## para ver que acertijos lleva, actualizar puntos y vigilar el fin de partida. 
## puede/debe de usar la misma template que la anterior, game.html

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


# vista que muestra el primer acertijo en game.html
@login_required
def game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    riddles = Riddle.objects.filter(game=game)
    return render(request, "game.html", {"riddles": riddles, "game": game})



# vista que maneja la respuesta del usuario al acertijo






















    







            
        
            


