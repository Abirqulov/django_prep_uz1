from django.contrib import admin
from .models import *
# Register your models here.


class AnswerAdminInline(admin.TabularInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    inlines = (AnswerAdminInline, )


admin.site.register(Category)
admin.site.register(Teachers)
admin.site.register(Lessons)
admin.site.register(Comment)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Course),
admin.site.register(ReaderLearns),
admin.site.register(RequirementsFromReader),