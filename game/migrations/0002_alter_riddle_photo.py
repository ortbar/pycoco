# Generated by Django 5.0.3 on 2024-08-08 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='riddle',
            name='photo',
            field=models.ImageField(upload_to='game_images'),
        ),
    ]