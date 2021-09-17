from ..models import *
from rest_framework import serializers


class Lesson_StructureSerializers(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()

    class Meta:
        model = Lesson_Structure
        fields = ['id', 'title', 'description', 'video']

    def get_description(self, lesson_structure):
        try:
            request = self.context.get('request')
            lan =request.GET.get('lan')
            description = lesson_structure.description
            if lan == "ru":
                description = lesson_structure.description_ru
                return description
            elif lan == "uz":
                description = lesson_structure.description
                return description
            else:
                return description
        except:
            return lesson_structure.description


class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'text', 'reply']


class QuestionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question', 'lesson']


class AnswerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'questions', 'answer', 'status']


class ResultsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Results
        fields = ['id', 'ques', 'ans']