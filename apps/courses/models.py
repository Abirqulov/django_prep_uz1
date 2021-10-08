from django.db import models
from account.models import *
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=120)
    name_ru = models.CharField(max_length=120)
    image = models.ImageField(upload_to='static/category_images')
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Teachers(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    description_ru = models.TextField()
    images = models.ImageField(upload_to='static/teachers_images')
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Course(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    teachers = models.ForeignKey(Teachers, on_delete=models.DO_NOTHING, blank=True)
    name = models.CharField(max_length=120)
    name_ru = models.CharField(max_length=120, null=True)
    price = models.CharField(max_length=120)
    description = models.TextField()
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Lessons(models.Model):
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.DO_NOTHING, related_name='lessons')
    name = models.CharField(max_length=120)
    name_ru = models.CharField(max_length=120)
    video = models.FileField(upload_to='static/videos', blank=True)
    parent = models.ForeignKey('self', related_name='childs', null=True, blank=True, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=120, null=True, blank=True, unique=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Lessons, on_delete=models.DO_NOTHING)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name="replies", null=True)

    def __str__(self):
        return str(self.author)


class Question(models.Model):
    lesson = models.ForeignKey(Lessons, on_delete=models.DO_NOTHING)
    text = models.CharField(max_length=120)
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer = models.CharField(max_length=150)
    ball = models.IntegerField(default=0)

    def __str__(self):
        return str(self.question)


