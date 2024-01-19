from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect , JsonResponse
from django.shortcuts import render
from django.urls import reverse

from django.core import serializers

from django.contrib.auth.decorators import login_required

import json

from .models import User , Post , Like , UserProfile , Notification

from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, "network/index.html")


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
            user_profile = UserProfile(user = user)
            user_profile.save()


        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


#Api views
@csrf_exempt
def get_posts_api_view(request):
    if request.method == "GET":
        data = []
        posts = Post.objects.all().order_by('-posted_at')
        for post in posts:
            data.append(post.serialize())
        return JsonResponse(data , safe= False)
    elif request.method == "POST":
        data = json.loads(request.body)
        print(data)
        post_data = data['user_post']
        new_post = Post(owner = request.user , text = post_data)
        new_post.save()
        return HttpResponse("Data Recieved")

@csrf_exempt
def get_likes_api_view(request):
    if request.method == "GET":
        data = []
        likes = Like.objects.filter(user = request.user)
        for like in likes:
            data.append(like.serialize())
        if len(data) == 0:
            return JsonResponse([{"None":"None"}] , safe = False , status = 204)
        return JsonResponse(data , safe= False)
    elif request.method == "POST":
        data = json.loads(request.body)
        current_post = Post.objects.get(id = data['post_id'])
        like = Like(post = current_post , user = request.user)
        current_post.likes += 1
        current_post.save()
        post_owner = User.objects.get(username = current_post.owner)
        post_owner.total_likes += 1
        post_owner.save()
        like.save()
        add_like_notification(current_post , request.user , "likes")
        return HttpResponse("recived")
    elif request.method == "DELETE":
        data = json.loads(request.body)
        likes = Like.objects.filter(post = data['post_id'] , user = request.user)
        for like in likes:
            like.delete()
        current_post = Post.objects.get(id = data['post_id'])
        current_post.likes -= 1
        current_post.save()
        post_owner = User.objects.get(username = current_post.owner)
        post_owner.total_likes -= 1
        post_owner.save()
        return HttpResponse("Deleted")


def get_following_posts_api_view(request):
    if request.method == 'GET':
        current_user_profile = UserProfile.objects.get(user = request.user)
        if current_user_profile is None:
            return JsonResponse([{"None":None}])
        data = []
        for following in current_user_profile.following.all():
            user_posts = Post.objects.filter(owner = User.objects.get(id = following.id))
            for post in user_posts:
                data.append(post.serialize())
        return JsonResponse(data , safe = False)

def following_posts_view(request):
    return render(request , "network/following.html")

def user_profile_view(request , request_user_name):
    current_user = User.objects.get(username = request_user_name)
    data = {
        "username" : current_user.username,
        "email" : current_user.email,
        "total_following" : current_user.number_of_following,
        "total_followers" : current_user.number_of_followers,
        "total_likes" : current_user.total_likes,
        "active" : current_user.is_active,
        "date_joined" : current_user.date_joined.date,
        "intro_bio" : current_user.intro_bio,
        "intro_body" : current_user.intro_body,
    }
    return render(request , "network/user.html" , data)


def get_user_post(request , request_user_name):
    if request.method == "GET":
         print("incoming request")
         latest_post = Post.objects.filter(owner= User.objects.get(username = request_user_name)).order_by('-posted_at')[:5]
         data = []
         for post in latest_post:
            data.append(post.serialize())
         return JsonResponse(data , safe = False)


def get_user_relation_view(request , request_user_name):
    if request.method == "GET":
     print("Recieving Data is User Relation View")
     status_data = {}
     if str(request.user) == str(request_user_name):
        print("runnn")
        status_data = {
            "status" : 1
        }
     else:
        current_user_profile = UserProfile.objects.get(user = User.objects.get(username = request.user))
        if current_user_profile._is_following_(request_user_name):
            status_data = {
                "status" : 2
            }
        else:
            status_data = {
                "status" : 3
            }
     print(status_data)
     return JsonResponse(status_data)

@csrf_exempt
def update_user_relation_api_view(request):
    if request.method == "PATCH":
        data = json.loads(request.body)
        target_user = User.objects.get(username = data['target_user'])
        current_user = User.objects.get(username = request.user)
        current_user_profile = UserProfile.objects.get(user = current_user)
        if current_user_profile._is_following_(target_user):
            current_user_profile.following.remove(target_user.id)
            target_user.number_of_followers -=1
            current_user.number_of_following -= 1
            current_user.save()
            target_user.save()
            current_user_profile.save()
        else:
            current_user_profile.following.add(target_user.id)
            target_user.number_of_followers += 1
            current_user.number_of_following += 1
            current_user.save()
            target_user.save()
            current_user_profile.save()
            add_following_notification(target_user , current_user)
        return HttpResponse("ok")


def add_like_notification(target_post , current_user):
    if target_post.owner != current_user:
     main_text = f"{current_user.username} liked your Post" 
     notification_demo = Notification(notification_post = target_post , notification_to = target_post.owner , text = main_text , notification_from = current_user )
     notification_demo.save()

def add_following_notification(target_user , current_user):
    main_text = f"{current_user} started Following you."
    notification_demo = Notification(notification_post = None , notification_to = target_user , text = main_text , notification_from = current_user)
    notification_demo.save()

def delete_notification(target_user , current_user , type):
    if target_post.owner != current_post:
        pass