from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser): # django의 AbstractUser Model을 상속받는다
    is_business = models.BooleanField(default=False)
    grade = models.CharField(max_length=10, default='C')