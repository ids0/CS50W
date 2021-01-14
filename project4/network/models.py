from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    likes = models.ManyToManyField('Post', through="Like",related_name="liked_posts")

    def __str__(self):
        return f"{self.username}"

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(blank=True)
    time = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField('User', through="Like")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "body": self.body,
            "time": self.time.strftime('%m/%d/%Y, %H:%M:%S'),
            "likes": len([0 for likes in self.likes.all()]) ,
        }

    def __str__(self):
        return f"{self.id} - User:{self.user} posted {self.body[0:15]} at - {self.time}"

class Follow(models.Model):
    # TODO: Make unique
    follower_id = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")
    following_id = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")
    time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower_id', 'following_id',)

    def __str__(self):
        return f"{self.follower_id} follows {self.following_id}"

class Like(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    # liked = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'post',)

    def __str__(self):
        return f"{self.user} liked {self.post}"
    # pass