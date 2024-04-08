from django.db import models
from django.contrib.auth.models import User

    
    
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
    photo_url = models.URLField()
    song_url = models.URLField()
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
