from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.core.paginator import Paginator

from django.http import JsonResponse

from .models import User, newPostForm, Post, Liked, Follow_user, Alert 
from .logic import count_likes, get_profile, paginate 
import json


def index(request):    
    posts = Post.objects.all().order_by('-date_created')
    posts = paginate(request, posts, 10)

    if request.method == 'POST':
        if request.user not in User.objects.all():
            return render(request, 'network/index.html', {
                'alert' : Alert('Please log in to post', 'danger', 'postError'),  
                'posts' : posts,
                'newPost' : newPostForm()
            })
    
        post = Post(user=request.user, content=request.POST['content'])
        post.save()

        return render(request, "network/index.html", {
            'newPost' : newPostForm(),
            'user_name' : request.user.username.capitalize(),
            'posts' : posts
        })

    else:    
        # page_number = request.GET.get('page')
        try: 
            return render(request, "network/index.html", {
                'newPost' : newPostForm(),
                'user_name' : request.user.username.capitalize(),
                'posts' : posts,
                'liked' : Liked.objects.filter(user=request.user)
            })
        except:
            return render(request, "network/index.html", {
                'newPost' : newPostForm(),
                'user_name' : request.user.username.capitalize(),
                'posts' : posts
            })

def user_profile_view(request, id):
    # might have to move this further down
    data = get_profile(request, id)

    data['posts'] = paginate(request, data['posts'], 10)

    if request.method == 'POST':
        if request.POST['follow']:
            request.user.follow(data['user'])
        else:
            request.user.unfollow(data['user']) 
        
        data = get_profile(request, id)
        data['posts'] = paginate(request, data['posts'], 10)

        return render(request, 'network/user.html', data)
    else:
        return render(request, 'network/user.html', data)

def following_posts_view(request):
    target_users = Follow_user.objects.filter(user=request.user)

    posts = []  
    for user in target_users:
        for post in Post.objects.filter(user=user.follow).order_by('-date_created'):
            posts.append(post)
    
    posts = paginate(request, posts, 10)

    return render(request, 'network/following.html', {
        'user_name': request.user.username.capitalize(),
        'posts' : posts
    })

def liked_api(request):
    if request.method == 'POST':

        # data from POST request at JS
        body = json.loads(request.body)

        # like    
        user = User.objects.get(pk=body['user_liked'])
        post = Post.objects.get(pk=body['post_liked'])

        create = False
        try:
            Liked.objects.get(user=user, post=post)
        except:
            create = True

        
        if create:
            instance = Liked(user=user, post=post)
            instance.save()

            likes = count_likes(post=post.id)
            
            return HttpResponse(json.dumps ({
                'user_liked' : user.id,
                'post_liked' : post.id,
                'like_count' : likes
            }))
        else:
            Liked.objects.get(user=user, post=post).delete()
            likes = count_likes(post=post.id)

            return HttpResponse(json.dumps ({
                'message' : 'deleted liked object',
                'like_count' : likes
            }))

        #return HttpResponse(request.body)
        

        # return the no. of likes 
        # return HttpResponseRedirect(reverse('index'))

    elif request.method == 'GET':
        # (as by GET method)

        # posts liked by user
        liked_by_user = Liked.objects.filter(user=request.user)

        # all posts 
        posts = Post.objects.all()

        # likes per post 
        liked_and_counts = {}
        for post in posts:
            liked_and_counts[post.id] = count_likes(post.id)

        return HttpResponse(json.dumps({
            'user_liked' : [liked.post.id for liked in liked_by_user],
            'likes_per_post' : liked_and_counts
        }))
    else:
        return HttpResponseRedirect(reverse('index'))

def get_user(request):
    return json.dumps({'user' : request.user})

def edit_post_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post_id = data['post_id'] 
        content = data['content'] 

        post = Post.objects.get(pk=post_id, user=request.user)
        post.edit_post(content)
        post.save()

        return HttpResponse()
    else:
        return HttpResponseRedirect(reverse('index'))

def post_view(request):
    try:
        posts = Post.objects.all()
    except:
        return JsonResponse({"error": "Posts not found"}, status=404)
    
    return JsonResponse([post.serialize() for post in posts], safe=False)

"""
def liked_view(request, post_id):    
    try:
        posts = Liked.objects.filter(post=post_id)
    except:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        return JsonResponse([post.serialize() for post in posts], safe=False)

    elif request.method == 'PUT':
        data = json.loads(request.body)
        if data.get("user") is not None:
            post.liked = data["liked"]
        post.save()
        return HttpResponse(status=204)
        
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)
"""

# register, login and logout

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
