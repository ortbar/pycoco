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
    photo = models.CharField(max_length=200, default='default_value')  # Añade un valor predeterminado    
    song_url = models.CharField(max_length=200) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.question
    
class Match(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.game.name
    
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
    


    

    

