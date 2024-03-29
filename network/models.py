from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    number_of_followers = models.IntegerField(default = 0)
    number_of_following = models.IntegerField(default = 0)
    total_likes = models.IntegerField(default = 0)
    pass
    intro_bio = models.CharField(max_length=150 , default = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
    intro_body = models.CharField(max_length= 200 , default =  "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident")
    is_verified = models.BooleanField(default = False)

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    posted_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    edited = models.BooleanField(default = False)
    likes = models.IntegerField(default = 0)

    def __str__(self):
        return f"{self.text} - {self.owner.username}" 
    
    def serialize(self):
        return {
            "id" : self.id,
            "owner" : self.owner.username,
            "text" : self.text,
            "posted_at" : self.posted_at,
            "edited" : self.edited,
            "likes" : self.likes,
            "verified":self.owner.is_verified
        }

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post} - {self.user}"
    
    def serialize(self):
        return {
            "post" : self.post.id
        }
    
class UserProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    follwers = models.ManyToManyField(User , related_name = 'followers' , null = True)
    following = models.ManyToManyField(User , related_name = 'following' , null = True)

    def __str__(self):
        return f"{self.user}"
    
    def _followers_count_(self):
        return self.follwers.count()
    
    def _following_count_(self):
        return self.following.count()
    
    def _is_following_(self , user_name):
        return self.following.filter(username = user_name).exists()

class Notification(models.Model):
    notification_post = models.ForeignKey(Post, on_delete=models.CASCADE , null = True)
    notification_to = models.ForeignKey(User , on_delete=models.CASCADE , related_name = "user_notfications")
    text = models.TextField()
    notification_from = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_date = models.DateTimeField( auto_now=False, auto_now_add=True)
    is_read = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.notification_from} - {self.notification_to}"
    
    def serialize(self):
        return {
            "notification_to" : self.notification_to.username ,
            "notification_text" : self.text,
            "notification_from" : self.notification_from.username ,
            "notification_date" : self.notification_date,
            "is_read" : self.is_read
        }

    
