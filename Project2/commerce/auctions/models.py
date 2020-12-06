from django.contrib.auth.models import AbstractUser
from django.db import models

categories = [
    ('Clothes', 'Clothes'),
    ('Games', 'Games'),
    ('Food', 'Food'),
]

class User(AbstractUser):
    pass
    # bids listings comments from related_name
    def __str__(self):
        return f"{self.username}"

# TODO: and watchlists

class Listing(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=512)
    img_url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    active = models.BooleanField(default=True) # Boolean
    time = models.DateTimeField(auto_now_add=True) # Time of when the listing was published
    initial_bid = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    category = models.CharField(max_length=16,choices=categories)
    
    def __str__(self):
        return f"Item: #{self.pk} - {self.title} from {self.user}"
    # Posible adds, another class for bid history, time of closing, etc.

class Bid(models.Model):
    amount = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    time = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Bid: #{self.pk} - {self.amount} for {self.listing} from {self.user}"

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=256)
    time = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Comment id: {self.pk} from {self.user} in {self.listing.title} at {self.time}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    added = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'item',)

    def __str__(self):
        return f"{self.pk}: {self.item.title} in {self.user} watchlist"
    