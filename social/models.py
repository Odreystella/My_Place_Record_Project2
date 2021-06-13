from django.db import models

from user.models import User
from behaviors import BaseField

class Relationship(BaseField):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='relationship')
    followers = models.ManyToManyField(User, blank=True, related_name='following')