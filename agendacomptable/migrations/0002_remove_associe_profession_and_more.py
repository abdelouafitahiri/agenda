# Generated by Django 5.0.9 on 2025-01-11 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agendacomptable', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='associe',
            name='profession',
        ),
        migrations.RemoveField(
            model_name='contratpersonnephysique',
            name='profession',
        ),
    ]