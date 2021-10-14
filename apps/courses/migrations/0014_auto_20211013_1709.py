# Generated by Django 3.2.7 on 2021-10-13 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0013_auto_20211013_1214'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReaderLearns',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('created_at', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RequirementsFromReader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='course',
            name='reader_obligation',
        ),
        migrations.RemoveField(
            model_name='course',
            name='you_learn',
        ),
    ]