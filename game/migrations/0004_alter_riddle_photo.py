# Generated by Django 5.0.3 on 2024-08-16 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_alter_riddle_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='riddle',
            name='photo',
            field=models.ImageField(upload_to='static/img'),
        ),
    ]