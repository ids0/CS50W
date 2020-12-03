from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    # bids listings comments from related_name
    def __str__(self):
        return f"{self.username}"



class Listing(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=512)
    img_url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    active = models.BooleanField(default=True) # Boolean
    time = models.DateTimeField(auto_now_add=True) # Time of when the listing was published
    initial_bid = models.DecimalField(max_digits=11, decimal_places=2, default=0)

    def __str__(self):
        return f"Item: #{self.pk} - {self.title} from {self.user}"
    # Posible adds, another class for bid history, time of closing, etc.

class Bid(models.Model):
    amount = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    time = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Bid: #{self.pk} - {self.amount} for {self.listing}"

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=256)
    time = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Comment id: {self.pk} from {self.user} in {self.listing.title}"

