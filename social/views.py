
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.http import JsonResponse
from django.core import serializers
import json

from social.services import CommentService
from place.services import PlaceService
from place.models import Place
from .dto import CommentCreateDto
from .models import Comment

class CommentCreateView(View):
    # def post(self, request, *args, **kwargs):
    #     post_pk = self.kwargs['pk']
    #     comment_dto = self._build_comment_dto(request)
    #     result = CommentService.create(comment_dto)
    #     return redirect('place:detail', post_pk)

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            print("ajax 요청 받기 성공")
            data = json.loads(request.body)

            comment_dto = self._build_comment_dto(request, data)
            # print(comment_dto)
            comment = CommentService.create(comment_dto)
            print("여기 통과 = DB에 댓글 인스턴스 생성")

            context = {
                'content' : comment.content,
                'created_string' : comment.created_string,
            }
            # ser_comment = serializers.serialize("json", [comment, context, ]) # 최근에 생성된 코멘트 인스턴스 한개 보내기
            # return JsonResponse({"new_comment": ser_comment}, status=200)
            return JsonResponse(context, status=200)
        else:
            return JsonResponse({"error": "Error occured during request" }, status=400)
                

    def _build_comment_dto(self, request, data):
        post_pk = data.get('post_pk')
        place = Place.objects.filter(pk=post_pk).first()
        return CommentCreateDto(
            place=place,
            commenter=request.user,
            content=data.get('content'),
            pk = data.get('post_pk')
        )

