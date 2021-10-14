from ..models import *
from rest_framework import serializers


class LessonSerializers(serializers.ModelSerializer):
    childs = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField()

    class Meta: 
        model = Lessons
        fields = ['id', 'course', 'name', 'video', 'childs', 'slug']

    def get_childs(self, instance):
        childs = instance.childs.all().order_by('id')
        request = self.context.get('request')
        return LessonSerializers(childs, many=True, context={'request': request}).data

    def get_name(self, lesson1):
       try:
           request = self.context.get('request')
           lan = request.GET.get('lan')
           name = lesson1.name
           if lan == 'ru':
               name = lesson1.name_ru
           elif lan == 'uz':
               name = lesson1.name
           return name
       except:
           return lesson1.name


class CourseTeacher(serializers.ModelSerializer):
    class Meta:
        model = Teachers
        fields = ['id', 'name']


class ReaderLearnsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReaderLearns
        fields = ['id', 'title']


class RequirementsFromReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequirementsFromReader
        fields = ['id', 'title']


class CourseListSerializers(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    lessons = LessonSerializers(many=True, read_only=True)
    teachers = CourseTeacher(many=False, read_only=True)
    course_reader = ReaderLearnsSerializer(many=True, read_only=True)
    course_requirements = RequirementsFromReaderSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'category', 'name', 'about', 'image', 'price', 'slug',
                  'course_reader', 'course_requirements', 'teachers', 'description', 'lessons']

    def get_name(self, course):
        request = self.context.get('request')
        lan = request.GET.get('lan', 'uz')
        if lan == 'uz':
            if course.name:
                return course.name
        elif lan == 'ru':
            if course.name_ru:
                return course.name_ru
        return course.name


class CourseIdSlugSerializers(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    lessons = LessonSerializers(many=True, read_only=True)
    teachers = CourseTeacher(many=False, read_only=True)
    course_reader = ReaderLearnsSerializer(many=True, read_only=True)
    course_requirements = RequirementsFromReaderSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'about', 'image', 'teachers', 'category', 'price', 'description', 'slug', 'lessons',
                  'course_reader', 'course_requirements']

    def get_name(self, course):
        request = self.context.get('request')
        lan = request.GET.get('lan', 'uz')
        if lan == 'uz':
            if course.name:
                return course.name
        elif lan == 'ru':
            if course.name_ru:
                return course.name_ru
        return course.name


class CourseCategorySerializers(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    # teacher_name = serializers.SerializerMethodField()
    teachers = CourseTeacher(many=False, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'category', 'name', 'image', 'teachers', 'price', 'slug']

    # def get_teacher_name(self, course):
    #     return course.teachers.name

    def get_name(self, course):
        request = self.context.get('request')
        lan = request.GET.get('lan', 'uz')
        if lan == 'uz':
            if course.name:
                return course.name
        elif lan == 'ru':
            if course.name_ru:
                return course.name_ru
        return course.name


class CategoryListSerializers(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'slug']

    def get_name(self, category):
        try:
            request = self.context.get('request')
            lan = request.GET.get('lan')
            name = category.name
            if lan == "ru":
                name = category.name_ru
            elif lan == "uz":
                name = category.name
            return name
        except:
            return category.name


class CategorySerializers(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    courses = CourseCategorySerializers(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'slug', 'courses']

    def get_name(self, category):
        try:
            request = self.context.get('request')
            lan = request.GET.get('lan')
            name = category.name
            if lan == "ru":
                name = category.name_ru
            elif lan == "uz":
                name = category.name
            return name
        except:
            return category.name


class TeachersSerializers(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    course = CourseCategorySerializers(many=True, read_only=True)

    class Meta:
        model = Teachers
        fields = ['id', 'name', 'description', 'images', 'slug', 'course']

    def get_description(self, teacher):
        request = self.context.get('request')
        lan = request.GET.get('lan', 'uz')
        if lan == "uz":
            if teacher.description:
                return teacher.description
        elif lan == "ru":
            if teacher.description_ru:
                return teacher.description_ru

        return teacher.description


class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'text', 'reply']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'answers']


class LessonsChildSerializers(serializers.ModelSerializer):
    comments = CommentSerializers(many=True, read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Lessons
        fields = ['id', 'name', 'video', 'comments', 'questions', 'slug']



