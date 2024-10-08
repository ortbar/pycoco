from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    
    path("", views.login, name="login"),
    path("register", views.register, name="register"),
    path("index", views.index, name="index"),   
    path("estadisticas", views.estadisticas, name="estadisticas"),
    path("logout", views.logout, name="logout"),
    path("profile", views.profile, name="profile"),
    path('game/<int:game_id>/', views.game, name='game'),  
    path('check_answer/<int:match_id>/', views.check_answer, name='check_answer'),
    path('next_riddle/<int:match_id>/', views.next_riddle, name='next_riddle'),  
      
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




