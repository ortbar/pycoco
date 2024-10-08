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
    # obtener el usuario
    user = request.user
    # obtener el juego
    game = get_object_or_404(Game, id=game_id)
    # crear match (y guardarlo en la base de datos) y pasarlo por el return para saber el id e ir actualizando los puntos
     # Crear un nuevo Match cada vez que se inicie el juego
    match = Match.objects.create(user=user, game=game, points=0, acertijos_vistos=[])

    # Filtrar acertijos que el usuario no ha visto aún (como es una nueva partida, todos los acertijos estarán disponibles)
    riddles = Riddle.objects.filter(game=game)

   

      # Preparar el contexto para la plantilla
    context = {
        'game': game,
        'match': match, 
        'riddles': riddles,  # Pasar todos los acertijos disponibles 
        'match_id': match.id
    }
    
    # Pasar el match para que esté disponible en el template
    return render(request, "game.html",context)

## crear un metodo que sea para el boton de next que le pases el id del match actual
## para ver que acertijos lleva, actualizar puntos y vigilar el fin de partida. 
## puede/debe de usar la misma template que la anterior, game.html

def check_answer(request, match_id):
    if request.method == 'POST':
        # Obtener la partida actual (Match)
        match = get_object_or_404(Match, id=match_id)

        # Obtener el acertijo actual basado en los que aún no ha visto
        riddles = match.game.riddle_set.exclude(id__in=match.acertijos_vistos)
        if riddles.exists():
            riddle = riddles.first()  # El siguiente acertijo no resuelto
        else:
            return JsonResponse({'status': 'finished', 'message': '¡Has completado todos los acertijos!'})

        # Obtener la respuesta del formulario
        respuesta_usuario = request.POST.get('respuesta', '').strip().lower()

        # Comparar la respuesta
        if respuesta_usuario == riddle.answer.lower():
            # Si es correcta, aumentar los puntos y marcar acertijo como resuelto
            match.points += 10
            match.acertijos_vistos.append(riddle.id)
            match.save()

            # Enviar respuesta correcta y la canción asociada
            return JsonResponse({
                'status': 'correct',
                'message': '¡Respuesta correcta!',
                'points': match.points,
                'song_url': riddle.song_file.url if riddle.song_file else None
            })
        else:
            # Si es incorrecta
            return JsonResponse({
                'status': 'incorrect',
                'message': 'Respuesta incorrecta. Intenta de nuevo.',
                'points': match.points
            })
    return JsonResponse({'status': 'error'}, status=400)



    


    

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






























    







            
        
            


