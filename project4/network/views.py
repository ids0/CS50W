import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
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

@csrf_exempt
@login_required
def post(request, page_number = 1):

    # Likes and updates
    if request.method == "PUT":
        data = json.loads(request.body)
        post_id = data["id"]

        if data["reason"] == "Like":
            try:
                post = Post.objects.get(id = post_id)

                # User is post creator
                if data['liked']:
                    # Create Like
                    Like.objects.get_or_create(user=request.user, post=post)
                else:
                    # Delete Like
                    print('deleted')
                    Like.objects.get(user=request.user, post=post).delete()

            # TODO: Not a single post
            except Post.DoesNotExist:
                return JsonResponse({"error":"Posts not found."}, status=404)

            # TODO: How to redirect 
            return HttpResponseRedirect(reverse('index'))
        if data['reason'] == "Update":
            try:
                post = Post.objects.get(id = post_id)
                if request.user.id == post.user.id:
                    post.body = data['body']
                    post.save()
            except Post.DoesNotExist:
                return JsonResponse({"error":"Posts not found."}, status=404)

            # TODO: How to redirect 
            return HttpResponseRedirect(reverse('index'))




    #If GET return posts
    if request.method == "GET":
        # List of post to display
        try:
            # All Posts
            posts = [post.serialize() for post in Post.objects.all().order_by("time").reverse()]
            
            # Add info to post json resoponse
            for post in posts:
                post_selected = Post.objects.get(id=post['id'])
                post["owned"] = False
                # User is author of post
                if post_selected.user.id == request.user.id:
                    liked = True
                    post["owned"] = True
                elif (Like.objects.filter(user = request.user, post = post_selected ).exists() ):
                    liked = True
                else:
                    liked = False

                post["liked"] = liked

            # Pagination

            p = Paginator(posts,10)
            
            return JsonResponse({'posts':p.page(page_number).object_list,'pages':p.num_pages},safe=False)

        # TODO: Not a single post
        except Post.DoesNotExist:
            return JsonResponse({"error":"Posts not found."}, status=404)


        

    #If POST save new post
    if request.method == "POST":

        # TODO: Validate info 
        data = json.loads(request.body)['body']
        user = request.user

        new_post = Post(user=user,body=data)
        new_post.save()

        # Auto like own post
        Like.objects.get_or_create(user=user, post=new_post)

        return HttpResponseRedirect(reverse('post'))


# User profile page
def user(request,username):
    return render(request, "network/profile.html",{
        "username":username
    })

# API
def user_profile(request,username,page_number = 1):
    # Follow 
    if request.method == "PUT":
        data = json.loads(request.body)
        print(data)
        user = User.objects.get(pk = data["id"])
        if data["follow_status"]:
            Follow.objects.create(follower_id = request.user, following_id = user )
        else:
            # Delete follow
            Follow.objects.get(follower_id = request.user, following_id = user ).delete()



        return HttpResponseRedirect(reverse('index'))


    # post json
    elif request.method == 'GET':
        try:
            # Get User
            user = User.objects.get(username = username)

            # Get posts from user
            posts = [post.serialize() for post in user.posts.order_by("time").reverse()]


            # Get followers and followees
            number_following = user.following.all().count()
            number_followers = user.followers.all().count()


            # Follow status and own profile
            follow_status = False
            own_profile = False
            if request.user.is_authenticated:
                if request.user.id == user.id:
                    own_profile = True
                elif request.user.id in [follower.follower_id.id for follower in user.followers.all()]:
                    follow_status = True

            if own_profile:
                for post in posts:
                    post["owned"] = True

            p = Paginator(posts,10)

            profile = {'posts': p.page(page_number).object_list,
                        'pages': p.num_pages,
                        'followers': number_followers,
                        'following': number_following,
                        'follows': follow_status,
                        'authenticate': request.user.is_authenticated,
                        'own_profile': own_profile,
                        'id':user.id}

            return JsonResponse(profile,safe=False)
        except User.DoesNotExist:
            # TODO: How to handle this, maybe js side with error, hide/show section
            profile = {'posts':[],'followers':-1,'following':-1}
            return JsonResponse(profile,safe=False, status=404)
    

# API
@login_required
def following_post(request,page_number = 1):
    try:
        user = User.objects.get(id=request.user.id)
        # Add users that the user follows
        users = [following.following_id for following in user.following.all()]
        # Add post form current user + following users
        posts = [post.serialize() for post in Post.objects.filter(user__in = users).order_by("time").reverse()]

        for post in posts:
            post["owned"] = False

        p = Paginator(posts,10)
        response = {'posts': p.page(page_number).object_list,
                    'pages': p.num_pages,
                    }
        return JsonResponse(response,safe=False)
    except User.DoesNotExist:
        return JsonResponse({"error":"Posts not found."}, status=404)


def following(request):
    if request.user.is_authenticated:
        return render(request, "network/following.html",{})
    return HttpResponseRedirect(reverse("index"))