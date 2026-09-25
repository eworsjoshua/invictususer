from django.db import models
from django.contrib.auth.models import User
import uuid


GENDER_CHOICE = (
    ('male', 'Male'),
    ('female', 'Female'),
)

class profile (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500, blank=True, null=True)
    profile_pics  = models.ImageField(upload_to="users-profile-image/") 
    fullname = models.CharField(max_length=255)
    username = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICE)

    def __str__(self):
        return self.user