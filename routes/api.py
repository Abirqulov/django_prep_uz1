from register.views import *
from django.urls import path
from config import settings
from django.conf.urls.static import static
from apps.courses.api.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login_view'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh_view'),
    path('logout/', LogOutAPIView.as_view(), name='logout_view'),
    path('register/', RegisterAPIView.as_view()),
    path('profile/', UserProfileApiView.as_view()),
    path('regions/', RegionApiView.as_view()),

    path('category/', CategoryListAPIView.as_view()),
    path('category/<int:pk>', CategoryDetailAPIView.as_view()),
    path('category/<str:slug>', CategorySlugAPIView.as_view()),
    path('teachers/', TeachersListView.as_view()),
    path('teachers/<int:pk>', TeachersAPIView.as_view()),
    path('teachers/<str:slug>', TeachersSlugView.as_view()),
    path('course/<int:pk>', CourseAPIView.as_view()),
    path('course/<str:slug>', CourseSlugView.as_view()),
    path('courses/', CourseListView.as_view()),
    path('lessons', LessonsListApiView.as_view()),
    path('lesson/<str:slug>', LessonsSlugView.as_view()),
    path('lesson-childs', LessonChildListApiView.as_view()),
    path('lesson-child/<int:pk>', LessonChildApiView.as_view()),

    path('statistic', StatisticApiView.as_view()),

    path('lesson_video/', videos_file, name='videos'),
    path('images/', image_file),

    path('comment/', comment),

    path('question/<int:lesson_id>', QuestionList.as_view()),
    path('question-check/<int:lesson_id>', QuestionCheck.as_view()),
    path('answer/', AnswerList.as_view()),


]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
