from django.contrib import admin
from .models import UserModel,Follow

# Register your models here.

admin.site.register(UserModel)
admin.site.register(Follow)
