from dataclasses import dataclass
from user.models import User
from place.models import Place
from .models import Comment

@dataclass
class CommentCreateDto():
    place : Place
    commenter : User
    content : str
    pk : str

