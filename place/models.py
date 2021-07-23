from django.db import models

from user.models import User
from behaviors import BaseField

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

class Place(BaseField):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='place')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='place')
    name = models.CharField(max_length=64)
    location = models.CharField(max_length=64)
    memo = models.TextField()
    best_menu = models.CharField(max_length=64)
    additional_info = models.CharField(max_length=200)
    stars = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='place')
    like_comments = models.ManyToManyField(User, blank=True, related_name='like_place')

    def __str__(self):
        return self.name

class Photo(models.Model):
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True, related_name='photo')
    image = models.ImageField(upload_to='images/', default='default.png', blank=True, null=True)




