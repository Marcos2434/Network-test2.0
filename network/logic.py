from .models import Post, User, Follow_user
from django.core.paginator import Paginator

def count_likes(post):
    post = Post.objects.get(pk=post)
    return post.liked_post.all().count()

def get_profile(request, id):
    # username
    target_user = User.objects.get(pk=id)

    # followers
    target_followers = target_user.followers.count()

    # following
    target_following = target_user.following.count()

    # user's posts is reverse chronological order  
    # posts = target_user.post_user
    posts = Post.objects.filter(user=target_user).order_by('-date_created')

    # for those who are signed in and are not themselves:
        # follow/unfollow button   
    
    try:
        Follow_user.objects.get(user=request.user, follow=target_user)
        following_btn = False
    except:
        following_btn = True

    return {
        'followers' : target_followers, 
        'following' : target_following,
        'posts' : posts,
        'username' : target_user.username.capitalize(),
        'user_name' : request.user.username.capitalize(),
        'self_profile' : request.user == target_user,
        'following_btn' : following_btn
    }

    # return HttpResponse(f'This is a profile page with id {id}, followers={target_followers}, following={target_following}, posts={posts}')

# modification of 
# https://docs.djangoproject.com/en/3.0/topics/pagination/
def paginate(request, data, amount):
    paginator = Paginator(data, amount)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj