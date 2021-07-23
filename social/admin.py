from django.contrib import admin

from social.models import Relationship, Comment

admin.site.register(Relationship)
admin.site.register(Comment)