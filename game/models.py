from asyncio.windows_events import NULL
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

from pycoco import settings

    
    
class Game(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    
class Riddle(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.CharField(max_length=50)
    clue = models.CharField(max_length=50)
    photo = models.ImageField( upload_to='img', null=True, blank=True) # Añade un valor predeterminado    
    photo_1 = models.ImageField( upload_to='img', null=True, blank=True) # Añade un valor predeterminado
    photo_2 = models.ImageField( upload_to='img', null=True, blank=True) # Añade un valor predeterminado
    song_url = models.CharField(max_length=200) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.question
    
class Match(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # inicializar los puntuacion de la partida a cero
    points = models.IntegerField(default=0)
    # atributo del modelo match que almacena los acertijos ya vistos
    acertijos_vistos = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"user.user_name - self.game.name"

class userProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField( upload_to='profile_pics')
    
    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.avatar.path)
    


    

    

