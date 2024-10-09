from django.db import models
from django.contrib.auth.models import AbstractUser


# User Model Definition


class User(AbstractUser):

    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("femal", "Female")

    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)
    user_photo = models.ImageField(blank=True)
    name = models.CharField(max_length=150, default="", blank=True)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices)
