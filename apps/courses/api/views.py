from ..models import *
from .serializers import *
from .filters import *
from register.serializers import *
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import generics, views, response, filters
from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count
from django.db.models.functions import TruncMonth
from register.models import User
from datetime import datetime
import json
import datetime
from django.utils import timezone


class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategoryListSerializers
    queryset = Category.objects.all()
    filter_backends = [FullTextSearchFilterBackend, DjangoFilterBackend]
    search_fields = ['name', '@full_name']
    PageNumberPagination.page_size = 200


class CategoryDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CategorySerializers
    queryset = Category.objects.all()

    def get_object(self):
        pk = Category.objects.get(pk=self.kwargs.get('pk'))
        return pk


class CategorySlugAPIView(generics.RetrieveAPIView):
    serializer_class = CategorySerializers
    queryset = Category.objects.all()

    def get_object(self):
        slug = self.kwargs.get('slug')
        stuff = get_object_or_404(Category, slug=slug)
        return stuff


class TeachersListView(generics.ListAPIView):
    serializer_class = TeachersSerializers
    queryset = Teachers.objects.all()
    filter_backends = [FullTextSearchFilterBackend, DjangoFilterBackend]
    search_fields = ['name', 'description']
    PageNumberPagination.page_size = 200


class TeachersAPIView(generics.RetrieveAPIView):
    serializer_class = TeachersSerializers
    queryset = Teachers.objects.all()

    def get_object(self):
        pk = Teachers.objects.get(pk=self.kwargs.get('pk'))
        return pk


class TeachersSlugView(generics.RetrieveAPIView):
    serializer_class = TeachersSerializers
    queryset = Teachers.objects.all()

    def get_object(self):
        slug = self.kwargs.get('slug')
        staff = get_object_or_404(Teachers, slug=slug)
        return staff


class CourseListView(generics.ListAPIView):
    serializer_class = CourseListSerializers
    queryset = Course.objects.all()
    filter_backends = (filters.SearchFilter, FullTextSearchFilterBackend)
    search_fields = ['name', 'description']
    PageNumberPagination.page_size = 200


class CourseAPIView(generics.RetrieveAPIView):
    serializer_class = CourseIdSlugSerializers
    queryset = Course.objects.all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)


class CourseSlugView(generics.RetrieveAPIView):
    lookup_field = 'slug'
    serializer_class = CourseIdSlugSerializers
    queryset = Course.objects.all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)

    def get_object(self):
        slug = self.kwargs.get('slug')
        staff = get_object_or_404(Course, slug=slug)
        return staff


class LessonsListApiView(generics.ListAPIView):
    serializer_class = LessonSerializers
    queryset = Lessons.objects.filter(slug__isnull=True)


class LessonsSlugView(generics.RetrieveAPIView):
    serializer_class = LessonSerializers
    queryset = Lessons.objects.filter(slug__isnull=True)

    def get_object(self):
        slug = self.kwargs.get('slug')
        staff = get_object_or_404(Lessons, slug=slug)
        return staff


class LessonChildListApiView(generics.ListAPIView):
    serializer_class = LessonsChildSerializers
    queryset = Lessons.objects.filter(parent__isnull=False)


class LessonChildApiView(generics.RetrieveAPIView):
    serializer_class = LessonsChildSerializers
    queryset = Lessons.objects.filter(parent__isnull=False)


class QuestionList(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    PageNumberPagination.page_size = 200

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        return qs.filter(lesson=self.kwargs['lesson_id'])


class AnswerList(generics.ListCreateAPIView):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    PageNumberPagination.page_size = 200


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


class StatisticApiView(views.APIView):

    def get(self, request):

        users = User.objects.all()
        questions = Question.objects.all()
        videos = Lessons.objects.all()
        courses = Course.objects.all()

        users_count = users.count()
        questions_count = questions.count()
        videos_count = videos.count()
        courses_count = courses.count()

        data = [{
            'users': users_count,
            'videos': videos_count,
            'questions': questions_count,
            'courses': courses_count,
        }]
        return JsonResponse(data, safe=False)


def videos_file(request):
    videos = Lessons.objects.all()
    return render(request, 'video.html', {'videos': videos})


def image_file(request):
    images = Teachers.objects.all()
    category_image = Category.objects.all()
    return render(request, 'video.html', {'images': images, 'category_image': category_image})


class TeachersSumAPIView(generics.RetrieveAPIView):

    def get(self, request):
        totalsumma = []
        course = []
        # teacher = Teachers.objects.get(id=3)
        # print(teacher)
        courses = Course.objects.filter().values('name')
        print(courses)

        for c in courses:
            course += c
        data = [{
            'courses': len(course),
        }]
        return JsonResponse(data, safe=False)


class TeacherStatisticApiView(views.APIView):

    def get(self, request, *args, **kwargs):
        try:
            teachers = Teachers.objects.all()
            data = []
            for item in teachers:
                count_course = item.course.all().count()
                all_course = item.course.all()
                total_price = 0
                for c in all_course:
                    pr = c.price
                    if pr == 'Bepul':
                        continue
                    total_price += int(pr)
                data.append({
                    'teacher': item.name,
                    'count_course': count_course,
                    'total_price': total_price,
            })
        except:
            pass
        return JsonResponse(data, safe=False)


# class UserCount(views.APIView):
#     serializer_class = UserCountSerializer
#
#     def get(self, request):
#
#         # month = float(request.data.get('month'))
#         # print(request.data.get('month'))
#         # users = User.objects.filter(date_joined__month=month).count()
#         # print(users)
#         # data = [{
#         #     'users': users
#         # }]
#         #
#         # return JsonResponse(data, safe=False)
#


@api_view(['GET'])
def UserCount(request):

    from django.db import connection

    order_by = request.GET.get('order_by', None)
    start_mode = request.GET.get('start_mode', None)
    end_mode = request.GET.get('end_mode', None)
    if order_by == 'time':
        order_by = 'years, mothd'
    elif order_by == '-time':
        order_by = 'years desc, mothd desc'
    else:
        order_by = ''
    sql1 = ''
    print(start_mode)
    int_start_mode = int(start_mode)
    if start_mode:
        start_year = datetime.datetime.fromtimestamp(int_start_mode).year
        print(start_year)
        start_month = datetime.datetime.fromtimestamp(int_start_mode).month
        print(start_month)
        sql1 = f'EXTRACT(YEAR FROM ru.date_joined) <= {start_year} or EXTRACT(MONTH FROM ru.date_joined) <= {start_month}'
    # sql2 = f'EXTRACT(YEAR FROM ru.date_joined) < {datetime.datetime.now().year} and ' \
    #        f'EXTRACT(MONTH FROM ru.date_joined) < {datetime.datetime.now().month}'
    # if end_mode:
    #     end_year = datetime.datetime.fromtimestamp(end_mode).year
    #     end_month = datetime.datetime.fromtimestamp(end_mode).month
    #     sql2 = f'EXTRACT(YEAR FROM ru.date_joined) < {end_year} and EXTRACT(MONTH FROM ru.date_joined) < {end_month}'

    sql = f"""select EXTRACT(MONTH FROM ru.date_joined) mothd, EXTRACT(YEAR FROM ru.date_joined) as years, count(*) from register_user ru
                where {sql1}
                group by years,  mothd order by {order_by};"""

    cursor = connection.cursor()
    try:
        result = []
        cursor.execute(sql, ['default'])
        rows = cursor.fetchall()
        if len(rows) > 0:
            for row in rows:
                print(row)
                result.append(
                    {
                        'month': row[0],
                        'year': row[1],
                        'count': row[2],
                    }
                )
        res = {
            'status': 1,
            'result': result,
        }
        return Response(res)

    except Exception as e:
        cursor.close



