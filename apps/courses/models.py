from django.db import models
from account.models import *
# Create your models here.


class Teachers(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    description_ru = models.TextField()
    images = models.ImageField(upload_to='static/teachers_images')

    def __str__(self):
        return self.name


class Category(models.Model):
    teachers = models.ForeignKey(Teachers, on_delete=models.DO_NOTHING, null=True, blank=True)
    name = models.CharField(max_length=120)
    name_ru = models.CharField(max_length=120)
    image = models.ImageField(upload_to='static/category_images')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='childs', on_delete=models.DO_NOTHING)
    slug = models.SlugField(max_length=120, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Lessons(models.Model):
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=120)
    name_ru = models.CharField(max_length=120)
    teachers = models.ForeignKey(Teachers, on_delete=models.DO_NOTHING)
    price = models.CharField(max_length=120)
    parent = models.ForeignKey('self', related_name='childs', null=True, blank=True, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Lesson_Structure(models.Model):
    title = models.ForeignKey(Lessons, null=True, blank=True, on_delete=models.DO_NOTHING)
    vodeo = models.FileField(upload_to='static/videos')
    description = models.TextField()
    description_ru = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title.name)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Lesson_Structure, on_delete=models.DO_NOTHING)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name="replies", null=True)

    def __str__(self):
        return str(self.author)


class Question(models.Model):
    lesson = models.ForeignKey(Lessons, on_delete=models.DO_NOTHING)
    question = models.CharField(max_length=120)
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question


class Answer(models.Model):
    questions = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    answer = models.CharField(max_length=150)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.questions)


class Results(models.Model):
    quest = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    ans = models.ForeignKey(Answer, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ques
