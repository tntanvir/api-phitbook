from django.db import models
from django.contrib.auth.models import User
from category.models import Category
# Create your models here.


class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    image=models.URLField(blank=True,null=True,max_length=500)
    title=models.CharField(max_length=100,unique=True)
    discription=models.TextField()
    publication_date=models.DateTimeField(auto_now_add=True)
    category=models.ManyToManyField(Category)
    
   
    def __str__(self):
        return f'{self.user.username}:{self.title}'
    

class Likes(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE ,related_name='likes')

    def __str__(self) :
        return f'{self.user.username} {self.post.title}'
    


class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    comment=models.TextField()
    comment_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.user.username} {self.post.title} '