from django.contrib import admin

from place.models import Category, Place, Photo, Tag

admin.site.register(Category)
admin.site.register(Place)
admin.site.register(Photo)
admin.site.register(Tag)
