from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.voter.username} voted for {self.post.title}"
    

class FormData(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    message = models.TextField(null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

