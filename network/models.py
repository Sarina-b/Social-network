from django.contrib.auth.models import AbstractUser
from django.db import models


# User(All Abstract users features)
# Post(Post_id(primary_key),username_of_poster(foreign_key) , content , like , date_posted)
# Profile(Profile_id(primary_key) , User_id(foreign_key , unique) , number_of_followers , number_of_followings)


class User(AbstractUser):
    pass


class Post(models.Model):
    username_of_poster = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    like = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.username_of_poster} , {self.date_posted} , {self.like} , {self.content}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='following', blank=True)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)

    def __str__(self):
        return f"{self.user} , {self.following} , {self.followers}"
