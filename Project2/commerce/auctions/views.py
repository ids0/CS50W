from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Watchlist

from django.forms import ModelForm

class NewListing(ModelForm):
    initial_bid = forms.FloatField(min_value=0.00) 
    class Meta:
        model = Listing
        fields = ['title','description','img_url','initial_bid','category']

class CloseListing(ModelForm):
    class Meta:
        model = Listing
        fields = ['active']

class NewBid(ModelForm):
    amount = forms.FloatField(min_value=0.00) 
    class Meta:
        model = Bid
        fields = ['amount']
        
class NewComment(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class AddWatchlist(ModelForm):
    class Meta:
        model = Watchlist
        fields = ['added']


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html",{
        "listings":listings
    })


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
    max_bid = listing.bids.all().order_by("amount").last()
    comments = Comment.objects.filter(listing=listing_id)
    # if request.user.is_authenticated:
    #     watchlist_status = Watchlist.objects.filter(user=request.user.id, item=listing_id).exists()
    # else:
    #     watchlist_status = False

    if request.method == 'POST':
        
        bid_form = NewBid(request.POST)
        comment_form = NewComment(request.POST)
        watchlist_form = AddWatchlist(request.POST)
        close_listing_form = CloseListing(request.POST)

        if bid_form.is_valid() and request.POST.get('bid'):
            # Check if bid is new max bid
            # TODO: Why XX.01 is not valid
            print(float(max_bid.amount),float(bid_form.cleaned_data['amount']))
            if float(max_bid.amount) < float(bid_form.cleaned_data['amount']):
                # Save new bid
                bid = bid_form.save(commit=False)
                bid.user = request.user
                bid.listing = listing
                bid.save()

                # After saving last bid, delete all except last one.
                User.objects.get(id=bid.user.id).bids.exclude(id=bid.id).delete()

                # Show bid success 
                return HttpResponseRedirect(reverse("listing", args=[listing_id]))
            else:
                # Show error
                return HttpResponseRedirect(reverse("listing", args=[listing_id]))

        elif comment_form.is_valid() and request.POST.get('comment'):
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.listing = listing
            comment.save()
            # Show comment success 
            return HttpResponseRedirect(reverse("listing", args=[listing_id]))

        elif watchlist_form.is_valid() and request.POST.get('watchlist'):
            # Form data
            watchlist_form = watchlist_form.save(commit=False)
            # Create or update entry
            watchlist = Watchlist.objects.get_or_create(user=request.user,item=listing)[0]
            watchlist.added = watchlist_form.added
            watchlist.save()
            # Show watchlist success
            return HttpResponseRedirect(reverse("listing", args=[listing_id]))

        elif request.user.is_authenticated and request.user == listing.user:
            
            if close_listing_form.is_valid():
    
                listing.active = close_listing_form.save(commit=False).active
                listing.save()
                return HttpResponseRedirect(reverse("listing", args=[listing_id]))            
        else:
            return HttpResponseRedirect(reverse("listing", args=[listing_id]))

    else:
        bid_form = NewBid(instance=max_bid)
        comment_form = NewComment()
        watchlist_form = AddWatchlist()
        close_listing_form=CloseListing()
        if request.user.is_authenticated :
            if Watchlist.objects.filter(user=request.user.id).exists() :
                watchlist_form = AddWatchlist(instance=Watchlist.objects.filter(user=request.user.id).last())

            if request.user == listing.user:
                close_listing_form=CloseListing(instance=listing)


        return render(request, "auctions/listing.html",{
            "listing":listing,
            "bid":max_bid,
            "bid_form":bid_form,
            "comment_form":comment_form,
            "watchlist_form":watchlist_form,
            "close_listing_form":close_listing_form,
            "comments":comments
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

def watchlist(request):
    watchlist_items = Watchlist.objects.filter(user=request.user)
    print(watchlist_items)
    return render(request, "auctions/watchlist.html",{
        "watchlist_items":watchlist_items
    })

# TODO: Bid constraints
# Watchlist page
# Categories page