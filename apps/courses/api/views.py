from ..models import *
from .serializers import *
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView, CreateAPIView
from django.shortcuts import render, redirect, reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend


class Lesson_StructureAPIView(GenericAPIView):
    serializer_class = Lesson_StructureSerializers
    queryset = Lesson_Structure.objects.all()


def videos_file(request):
    videos = Lesson_Structure.objects.all()
    return render(request, 'video.html', {'videos': videos})


def image_file(request):
    images = Teachers.objects.all()
    category_image = Category.objects.all()
    return render(request, 'video.html', {'images': images, 'category_image': category_image})

#
# def category_images(request):
#     return render(request, 'video.html', {})

@api_view(['POST'])
def post_detail(request):
    post = request.data.get('post')
    if request.method == "POST":

        reply_obj = None
        try:
            reply_id = int(request.POST.get('reply_id'))
        except:
            reply_id = None
        if reply_id:
            reply_obj = Comment.object.get(id=reply_id)
        # reply = request.data.get['reply']
        author = request.data.get['author']
        comment = request.data.get['comment']
        if reply_obj:
            Comment(author=author, text=comment, reply=reply_obj, post=post).save()
        else:
            Comment(author=author, text=comment, post=post).save()
        Comment.save()
        res = {
            'status': 1,
        }
        return Response(res)
    else:
        serializers = CommentSerializers()
    comments = Comment.objects.filter(post=post, reply=None).order_by('-date_created')
    context = {
        'post': post,
        'serializers': serializers,
        'comments': comments
    }
    return Response(context)


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
        post=Lesson_Structure.objects.filter(id=int(post)).first(),
        author=User.objects.filter(id=int(author)).first(),
        text=str(text),

    )
    comment.save()
    res = {
        'status': 1,
    }
    return Response(res)


# class AnswerAPIView(generics.ListCreateAPIView):
#     serializer_class = AnswerSerializers
#
#     def get_queryset(self):
#         answer = Answer.objects.all()
#         return answer
#
#     def create(self, request, *args, **kwargs):
#         answer_data = request.data
#         status = True
#         if status:
#             ans = Answer.objects.create(question=answer_data['question'], answer=answer_data['answer'],
#                                         user=answer_data['user'])
#             ans.save()
#             return Response(ans)
#         else:
#             return


class QuestionAPIView(generics.ListAPIView):
    serializer_class = QuestionSerializers
    queryset = Question.objects.all()


class ResultAPIView(generics.GenericAPIView):
    serializer_class = ResultsSerializers

    def create(self, request):
        ques = request.data.get('ques')
        ans = request.data.get('ans')
        status = True
        if status:
            result = Results.objects.create(
                ques=Question.objects.filter(id=int(ques)).first(),
                ans=Answer.objects.filter(id=int(ans)).first(),
                status=Answer.objects.get('status')
            )
            result.save()
        else:
            pass



