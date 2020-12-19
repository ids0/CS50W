from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.id} - {self.username}"

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(blank=True)
    time = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "body": self.body
        }

    def __str__(self):
        return f"{self.id} - User:{self.user} posted {self.body[0:15]} at {self.time}"

class Follow(models.Model):
    # TODO: Make unique
    follower_id = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")
    following_id = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower_id} follows {self.following_id}"

class Like(models.Model):
    # TODO: Make unique
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="likes")

