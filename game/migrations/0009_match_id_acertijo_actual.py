# Generated by Django 5.0.3 on 2024-10-16 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0008_remove_riddle_created_at_remove_riddle_song_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='id_acertijo_actual',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
