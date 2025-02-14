from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.

"""
This is better to set blank=True/False and null=True/False for all of the fields.
"""


class Bolg_User(AbstractUser):  # name of models must be start with capital and does not contain _.
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='media/profile_pics/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # why in this way?
    image = models.ImageField(upload_to='media/post_images/', blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

