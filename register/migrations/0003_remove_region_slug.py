# Generated by Django 3.2.9 on 2021-11-08 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_region_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='region',
            name='slug',
        ),
    ]