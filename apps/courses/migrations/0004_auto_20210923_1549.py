# Generated by Django 3.2.7 on 2021-09-23 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_rename_category_lessons_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='user',
        ),
        migrations.AlterField(
            model_name='lessons',
            name='video',
            field=models.FileField(blank=True, upload_to='static/videos'),
        ),
    ]
