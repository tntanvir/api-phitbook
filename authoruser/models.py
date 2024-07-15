
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserModel(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.URLField(blank=True,null=True,max_length=500)
    phone_number=models.CharField(max_length=12)
    location=models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
