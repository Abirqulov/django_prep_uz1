# Generated by Django 3.2.7 on 2021-10-12 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_lessons_k'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lessons',
            name='k',
        ),
    ]
