from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment

from django.forms import ModelForm
class NewListing(ModelForm):
   class Meta:
        model = Listing
        fields = ['title','description','img_url','initial_bid']



def index(request):
    return render(request, "auctions/index.html")


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    bid = listing.bids.all().first()
    return render(request, "auctions/listing.html",{
        "listing":listing,
        "bid":bid
    })

def new_listing(request):

    if request.method == 'POST':
        form = NewListing(request.POST)
        if form.is_valid():
            # user = request.user
            # listing = Listing(user=user)
            # form = NewListing(request.POST, instance=listing)
            # form.save()
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return HttpResponseRedirect(reverse("listing", args=[listing.id]))
    
    else:
        forms = NewListing()

        return render(request, "auctions/new_listing.html",{
            "forms":forms
        })


    # test = Listing.objects.get(pk=1) #Edit
    # forms =NewListing(instance=test)

    # TODO: Make a bid in listing page
    # TODO: Make a comment on listing page
    # TODO: index.html