from django.db.models import CASCADE
from django.db import models

# Create your models here.


class User(models.Model):
    email = models.EmailField("Email")
    username = models.CharField(max_length=50)


class Comment(models.Model):
    user = models.ForeignKey(to=User, on_delete=CASCADE, related_name="comment")
    content = models.CharField(max_length=200)
    created = models.DateTimeField()
