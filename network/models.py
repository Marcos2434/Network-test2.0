from django.contrib.auth.models import AbstractUser
from django.db import models

from django import forms
from django.utils import timezone



# models 

class User(AbstractUser):
    def follow(self, follow_user):
        try:
            Follow_user.objects.get(user=self, follow=unfollow_user)
        except:
            Follow_user.objects.create(user=self, follow=follow_user)
    def unfollow(self, unfollow_user):
        Follow_user.objects.get(user=self, follow=unfollow_user).delete()

class Follow_user(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    follow = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f"{self.user} is following {self.follow}"
    
    class Meta:
        unique_together = ('user', 'follow')

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_user')
    content = models.CharField(max_length=600)

    date_created = models.DateTimeField(default=timezone.now)

    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'date_created': self.date_created,
            'userId': self.user.id
        }
    
    def edit_post(self, new_content):
        self.content = new_content
    
    def __str__(self):
        return f"{self.user}'s post with id {self.id}"
        # return f"{self.user}'s post with id {self.id} created on {self.date_created}"

class Liked(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='liked_post')

    def __str__(self):
        return f"{self.post.user}'s no.{self.post.id} post has been liked by {self.user}"
    
    def serialize(self):    
        return {
            'id': self.id,
            'userId': self.user.id,
            'postId': self.post.id
        }
    
    #https://docs.djangoproject.com/en/dev/topics/db/models/#meta-options
    class Meta:
        unique_together = ('user', 'post')


class newPostForm(forms.Form):

    content = forms.CharField(
        label="", 
        widget=forms.Textarea,
        max_length=600
    )

    content.widget.attrs.update({
        'id':'newPost',
        'class':'form-control',
        'placeholder':"What's on your mind?"
    })

class Alert():
    def __init__(self, message, color, extra=''):
        self.message = message
        self.color = color
        self.extra = extra

# alert = Alert('Added to your Watch List', 'info', 'watchList')  



