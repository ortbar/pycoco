# Generated by Django 5.0.3 on 2024-10-16 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0009_match_id_acertijo_actual'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='id_acertijo_actual',
        ),
    ]