from social.dto import CommentCreateDto
from user.models import User
from place.models import Place
from .models import Comment
from utils import build_error_msg, build_success_msg

class CommentService():
    
    @staticmethod
    def find_comments(place_pk):
        return Comment.objects.filter(place__pk=place_pk)

    @staticmethod
    def create(dto:CommentCreateDto):
        if not dto.content:
            return build_error_msg('MISSING_INPUT')
        comment = Comment.objects.create(
            place=dto.place,
            commenter=dto.commenter,
            content=dto.content
        )
        return comment