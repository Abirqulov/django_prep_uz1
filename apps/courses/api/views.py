from ..models import *
from .serializers import *
from .filters import *
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView, CreateAPIView, RetrieveAPIView
from django.shortcuts import render, redirect, reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics, views, response
from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend


class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategoryListSerializers
    queryset = Category.objects.all()
    filter_backends = [FullTextSearchFilterBackend, DjangoFilterBackend]
    search_fields = ['name', '@full_name']


class CategoryDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CategorySerializers
    queryset = Category.objects.all()
    filter_backends = [FullTextSearchFilterBackend, DjangoFilterBackend]
    search_fields = ['name', '@full_name']

    def get_object(self):
        pk = Category.objects.get(pk=self.kwargs.get('pk'))
        return pk


class CategorySlugAPIView(generics.RetrieveAPIView):
    serializer_class = CategorySerializers
    queryset = Category.objects.all()
    filter_backends = [FullTextSearchFilterBackend, DjangoFilterBackend]
    search_fields = ['name', '@full_name']

    def get_object(self):
        slug = self.kwargs.get('slug')
        stuff = get_object_or_404(Category, slug=slug)
        return stuff


class TeachersListView(generics.ListAPIView):
    serializer_class = TeachersSerializers
    queryset = Teachers.objects.all()
    filter_backends = [FullTextSearchFilterBackend, DjangoFilterBackend]
    search_fields = ['name', '@full_name']


class TeachersAPIView(generics.RetrieveAPIView):
    serializer_class = TeachersSerializers
    queryset = Teachers.objects.all()

    def get_object(self):
        pk = Teachers.objects.get(pk=self.kwargs.get('pk'))
        return pk


class TeachersSlugView(generics.RetrieveAPIView):
    serializer_class = TeachersSerializers
    queryset = Teachers.objects.all()
    filter_backends = [FullTextSearchFilterBackend, DjangoFilterBackend]
    search_fields = ['name', '@full_name']

    def get_object(self):
        slug = self.kwargs.get('slug')
        staff = get_object_or_404(Teachers, slug=slug)
        return staff


class CourseAPIView(generics.RetrieveAPIView):
    serializer_class = CourseSerializers
    queryset = Course.objects.all()
    filter_backends = [FullTextSearchFilterBackend, DjangoFilterBackend]
    search_fields = ['name', '@full_name']
    #
    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset()
    #     return qs.filter(category=self.kwargs['category_id'])


class CourseSlugView(generics.RetrieveAPIView):
    serializer_class = CourseSerializers
    queryset = Course.objects.all()

    def get_object(self):
        slug = self.kwargs.get('slug')
        staff = get_object_or_404(Course, slug=slug)
        return staff


class LessonsAPIView(generics.ListAPIView):
    serializer_class = LessonSerializers
    queryset = Lessons.objects.filter(parent__isnull=True)
    filter_backends = (FullTextSearchFilterBackend, DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ['name', '@full_name', 'teachers']


class LessonsSlugView(generics.RetrieveAPIView):
    serializer_class = LessonSerializers
    queryset = Lessons.objects.filter(slug__isnull=True)

    def get_object(self):
        slug = self.kwargs.get('slug')
        staff = get_object_or_404(Lessons, slug=slug)
        return staff


class QuestionList(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        return qs.filter(lesson=self.kwargs['lesson_id'])


class AnswerList(generics.ListCreateAPIView):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()


class QuestionCheck(views.APIView):

    def post(self, request, lesson_id):
        print(request.data, lesson_id)
        answers = request.data.get('answers', [])
        questions = Question.objects.filter(lesson=lesson_id).values('id', 'answers__id', 'answers__ball')
        answer = []
        question = []
        bal = 0
        max_ball = 0
        count = 0
        print(questions)
        for q in questions:
            max_ball += q['answers__ball']
            for a in answers:
                if q['id'] == a['question'] and a['answer'][0] == q['answers__id']:
                    bal += q['answers__ball']
                    if a['answer'][0] == q['answers__id'] and q['answers__ball'] != 0:
                        if q['id'] not in question:
                            question.append(q['id'])
                        answer.append(q['answers__id'])
                        count += 1
        return response.Response({
            'ball': bal,
            'max_ball': max_ball,
            'question': question,
            'answer': answer,
            'count': count,
        })


@api_view(['POST'])
def comment(request):
    post = request.data.get('post')
    author = request.data.get('author')
    text = request.data.get('text')
    reply_id = request.data.get('reply_id')
    reply = None
    if reply_id:
        reply = Comment.objects.filter(id=reply_id).first()
    comment = Comment.objects.create(
        reply=reply,
        post=Lessons.objects.filter(id=int(post)).first(),
        author=User.objects.filter(id=int(author)).first(),
        text=str(text),

    )
    comment.save()
    res = {
        'status': 1,
    }
    return Response(res)



def videos_file(request):
    videos = Lessons.objects.all()
    return render(request, 'video.html', {'videos': videos})


def image_file(request):
    images = Teachers.objects.all()
    category_image = Category.objects.all()
    return render(request, 'video.html', {'images': images, 'category_image': category_image})

