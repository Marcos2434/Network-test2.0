from django.contrib import admin
from .models import Post, User, Liked, Alert, Follow_user


# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Liked)
admin.site.register(Follow_user)
