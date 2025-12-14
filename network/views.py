import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Profile


def index(request):
    posts = Post.objects.all().order_by('-date_posted')
    return render(request, 'network/index.html', {'posts': posts})


@login_required
def following_posts(request):
    following_users = Profile.objects.get(user=request.user).following.all()
    posts = Post.objects.filter(username_of_poster__in=following_users).order_by('-date_posted')
    return render(request, 'network/index.html', {'posts': posts})


def not_login(request):
    return render(request, 'network/not_login.html')


@csrf_exempt
@login_required
def user_info(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        clicked_user_id = data['clicked_user_id']
        clicked_user = User.objects.get(pk=clicked_user_id)
        clicked_user_profile = Profile.objects.get(user=clicked_user)
        if data['follow']:
            Profile.objects.get(user=request.user).following.add(clicked_user)
        else:
            Profile.objects.get(user=request.user).following.remove(clicked_user)

        clicked_user_following = clicked_user_profile.following.count()
        clicked_user_followers = Profile.objects.filter(following=clicked_user).count()

        return JsonResponse({'clicked_user_following': clicked_user_following,
                             'clicked_user_followers': clicked_user_followers})


def profile(request, username):
    clicked_user = User.objects.get(username=username)
    posts = Post.objects.filter(username_of_poster=clicked_user).order_by('-date_posted')
    count_following = clicked_user.profile.following.count()
    count_followers = Profile.objects.filter(following=clicked_user).count()
    activate_follow_or_unfollow = request.user != clicked_user
    in_following = request.user.profile.following.filter(id=clicked_user.id).exists()
    if in_following:
        in_following = True
    else:
        in_following = False
    return render(request, 'network/index.html',
                  {'posts': posts, 'count_following': count_following,
                   'count_followers': count_followers, 'activate_follow_or_unfollow': activate_follow_or_unfollow
                      , 'in_following': in_following, 'is_profile_page': True, 'clicked_user': clicked_user})


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


@csrf_exempt
@login_required
def create_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get('content', '')
        if content == '':
            return JsonResponse({
                "error": "Content cannot be empty."
            }, status=400)
        new_post = Post(username_of_poster=request.user, content=content)
        new_post.save()
        return JsonResponse({
            "success": "Post created successfully."
        }, status=200)
    else:
        return render(request, 'network/create_post.html')
