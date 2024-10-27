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

    # match = Match.objects.get(user=user, game=game, partida_terminada=False)

    # if (type(match) == list and len(match) > 1):
    #     # Código para manejar el caso en que la lista de partidas sea mayor a 1
    #     pass  # Reemplaza "pass" con el código que necesites ejecutar
    #     dar error de que hay varias partidas inacabadas y borrarlas todas y reiniciar juego por ejemplo

    # elif (type(match) == list and len(match) == 1):
    #     match = match[0]
    # else:
    #     # Crear nueva partida
    #     match = Match.objects.create(user=user, game=game, points=0, acertijos_vistos=[])


    
   
    #  Buscar una partida no terminada para el usuario y el juego en curso 
    match = Match.objects.filter(user=user, game=game, partida_acabada=False).first()

     # si no existe una partida no terminada, crear una nueva
    if not match:
        match = Match.objects.create(user=user, game=game, points=0, acertijos_vistos=[])

    # Verificar si hay un acertijo en curso, si no, seleccionar el siguiente disponible
    if not match.acertijo_corriente and not match.partida_acabada:
    # Obtener el siguiente acertijo no visto        
        riddles = Riddle.objects.filter(game=game).exclude(id__in=match.acertijos_vistos)
        if riddles.exists():
            match.acertijo_corriente = riddles.first() # seleccionar el primer acertijo no visto
            match.acertijo_resuelto = False
            match.save()
        else:
            match.partida_acabada = True
            match.save() 
   

      # Preparar el contexto para la plantilla
    context = {
        'game': game,
        'match_id': match.id,
        'match': match,  
        'riddle': match.acertijo_corriente, # pasar el acertijo corriente a la plantilla
        'acertijo_resuelto': match.acertijo_resuelto # pasar el estado de si el acertijo ha sido resuelto
    }
    
    # Pasar el match para que esté disponible en el template
    return render(request, "game.html",context)

## crear un metodo que sea para el boton de next que le pases el id del match actual
## para ver que acertijos lleva, actualizar puntos y vigilar el fin de partida. 
## puede/debe de usar la misma template que la anterior, game.html


##¿Qué hace esta vista check_answer?:

    ##1 Recibe una solicitud GET para obtener el siguiente acertijo.
    ##2 Filtra los acertijos que no han sido vistos por el usuario.
    ##3 Si encuentra un acertijo, lo envía en formato JSON.
    ##4 Si no encuentra más acertijos, devuelve un mensaje de que el juego ha terminado.


def check_answer(request, match_id):
    if request.method == 'POST':
        # Obtener la partida actual (Match)
        match = get_object_or_404(Match, id=match_id)

        # Verificar si hay un acertijo corriente y que la partida no esté terminada
        riddle = match.acertijo_corriente
        if not riddle or match.partida_acabada:
            return JsonResponse({'status': 'error', 'message': 'No hay acertijo activo o la partida ha finalizado.'})
        
        # Obtener la respuesta del usuario
        respuesta_usuario = request.POST.get('respuesta', '').strip().lower()
        respuesta_correcta = riddle.answer.strip().lower()

        # Verificar si la respuesta es correcta
        if respuesta_usuario == respuesta_correcta:
            # Aumentar los puntos y marcar el acertijo como resuelto
            match.points += 10
            match.acertijos_vistos.append(riddle.id)
            match.acertijo_resuelto = True  # Marcar como resuelto
            # Guardar el estado de la partida sin avanzar al siguiente acertijo
            match.save()

            # Responder con éxito y reproducir la canción
            return JsonResponse({
                'status': 'correct',
                'message': '¡Respuesta correcta!',
                'points': match.points,
                'song_url': riddle.song_file.url if riddle.song_file else None
            })
        else:
            # Si la respuesta es incorrecta, restar puntos y mantener el acertijo actual
            match.points -= 2
            match.save()  # Guardar los cambios

            # Responder con error
            return JsonResponse({
                'status': 'incorrect',
                'message': 'Respuesta incorrecta. Se han restado 2 puntos. Inténtalo de nuevo.',
                'points': match.points
            })

    # Respuesta en caso de que no sea un método POST
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=400)





from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def next_riddle(request, match_id):
    if request.method == 'GET':
        # Obtener la partida actual (Match)
        match = get_object_or_404(Match, id=match_id)

        # Verificar si la partida ya ha terminado
        if match.partida_acabada:
            return JsonResponse({'status': 'finished', 'points': match.points})

        # Verificar si el acertijo actual está resuelto
        if not match.acertijo_resuelto:
            return JsonResponse({'status': 'error', 'message': 'El acertijo actual no ha sido resuelto.'})

        # Buscar el siguiente acertijo no resuelto
        siguiente_acertijo = Riddle.objects.filter(
            game=match.game
        ).exclude(id__in=match.acertijos_vistos).first()  # Utilizar first() para obtener un solo objeto Riddle

        # Verificar si se encontró un siguiente acertijo
        if siguiente_acertijo:
            # Actualizar el acertijo corriente y el estado de resuelto
            match.acertijo_corriente = siguiente_acertijo
            match.acertijo_resuelto = False
            match.save()

            # Responder con los detalles del siguiente acertijo
            return JsonResponse({
                'status': 'next_riddle',
                'question': siguiente_acertijo.question,
                'photo': siguiente_acertijo.photo.url if siguiente_acertijo.photo else None,
                'photo_1': siguiente_acertijo.photo_1.url if siguiente_acertijo.photo_1 else None,
                'photo_2': siguiente_acertijo.photo_2.url if siguiente_acertijo.photo_2 else None,
                'points': match.points
            })
        else:
            # Si no hay más acertijos, marcar la partida como finalizada
            match.acertijo_corriente = None
            match.partida_acabada = True
            match.save()

            # Responder con el estado de finalización
            return JsonResponse({'status': 'finished', 'points': match.points})

    # Respuesta en caso de que no sea un método GET
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=400)



        
        # si no hay mas acertijos se marca la partida como terminada










    


    

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






























    







            
        
            


