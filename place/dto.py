from dataclasses import dataclass

from user.models import User
from place.models import Category

@dataclass
class CreateDto():
    category : Category
    author : User 
    name : str
    location : str
    memo : str
    best_menu : str
    additional_info : str
    stars : str
    # tag : str
    image : list 
    pk : str


@dataclass
class UpdateDto():
    name : str
    location : str
    stars : str
    memo : str
    best_menu : str
    additional_info : str
    image : list
    pk : str