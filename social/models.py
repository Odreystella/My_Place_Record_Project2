import time
import datetime
from django.db import models

from user.models import User
from place.models import Place
from behaviors import BaseField


class Relationship(BaseField):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='relationship')
    followers = models.ManyToManyField(User, blank=True, related_name='following')


class Comment(BaseField):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='comment')
    commenter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='comment')
    content = models.TextField()

    def __str__(self):
        return self.content

    @property
    def created_string(self):
     
      now = datetime.datetime.now()
      datetime_format = now.strftime('%Y-%m-%d %H:%M:00')
      current_date = time.mktime(time.strptime(datetime_format,'%Y-%m-%d %H:%M:%S'))

      time_passed = int(float(current_date))-int(float(self.created_at))
    #   print(time_passed)
      if time_passed == 0:
          return '1분 전'
      if time_passed < 60:
          return str(time_passed) + '분 전'
      if time_passed//60 < 60:
          return str(int(time_passed//60)) + '분 전'
      if time_passed//(60*60) < 24:
          return str(int(time_passed//(60*60))) + '시간 전'
      if time_passed//(60*60*24) < 30:
          return str(int(time_passed//(60*60*24))) + '일 전'
      if time_passed//(60*60*24*30) < 12:
          return str(int(time_passed//(60*60*24*30))) + '달 전'
      else:
          return '오래 전'  
