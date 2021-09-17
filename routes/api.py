from account.api.views import *
from django.urls import path
from apps.courses.api.views import *


urlpatterns = [
    path('users/', UsersView.as_view()),
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),

    path('lesson_structure/', Lesson_StructureAPIView.as_view()),
    path('lesson_video/', videos_file, name='videos'),
    path('images/', image_file),

    path('post_detail/', post_detail),
    path('comment/', comment),

    # path('answer/', AnswerAPIView.as_view()),
    path('question/<int:pk>', QuestionAPIView.as_view()),
    path('results/', ResultAPIView.as_view()),
    # path('answer_fun/', answer),
]
