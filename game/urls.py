from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    
    path("", views.login, name="login"),
    path("register", views.register, name="register"),
    path("index", views.index, name="index"),   
    path("game", views.game, name="game"),
    path("estadisticas", views.estadisticas, name="estadisticas"),
    path("logout", views.logout, name="logout"),
    path("profile", views.profile, name="profile"),
    

    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)