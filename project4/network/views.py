import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Like, Follow


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
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

# @csrf_exempt
@login_required
def post(request):


    try:
        user = User.objects.get(id=request.user.id)
        posts = []
        for following in user.following.all():
            for post in following.following_id.posts.all():
                posts.append(post.serialize())

    except User.DoesNotExist:
        return JsonResponse({"error":"Posts not found."}, status=404)

    print(posts)
    #If GET return posts
    if request.method == "GET":
        return JsonResponse(posts,safe=False)

    #If POST save new post
    if request.method == "POST":

        # TODO: Validate info 
        data = json.loads(request.body)['body']
        user = request.user

        new_post = Post(user=user,body=data)
        new_post.save()


        
        return HttpResponseRedirect(reverse('post'))