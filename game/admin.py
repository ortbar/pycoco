from django.contrib import admin
from .models import *

# Register your models here/registrar mis modelos aquí. hay que poner esto aqui para que se muestren en el admin
admin.site.register(Game)
admin.site.register(Riddle)
admin.site.register(Match)



