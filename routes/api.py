from account.api.views import *
from django.urls import path
from apps.courses.api.views import *


urlpatterns = [
    path('users/', UsersView.as_view()),
    path('register/', RegisterApiView.as_view()),
    path('login/', LoginApiView.as_view()),

    path('category/', CategoryListAPIView.as_view()),
    path('category/<int:pk>', CategoryDetailAPIView.as_view()),
    path('category/<str:slug>', CategorySlugAPIView.as_view()),
    path('teachers/', TeachersListView.as_view()),
    path('teachers/<int:pk>', TeachersAPIView.as_view()),
    path('teachers/<str:slug>', TeachersSlugView.as_view()),
    path('course/<int:pk>', CourseAPIView.as_view()),
    path('course/<str:slug>', CourseSlugView.as_view()),
    path('courses/', CourseListView.as_view()),
    path('lesson/<str:slug>', LessonsSlugView.as_view()),

    path('lesson_video/', videos_file, name='videos'),
    path('images/', image_file),

    path('comment/', comment),

    path('question/<int:lesson_id>', QuestionList.as_view()),
    path('question-check/<int:lesson_id>', QuestionCheck.as_view()),
    path('answer/', AnswerList.as_view()),


]
