
from rest_framework import serializers
from .models import Post,Comment,Likes
     

class AllComments(serializers.ModelSerializer):
    class Meta:
        model=Comment
        read_only_fields=['user']
        fields='__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Likes
        fields='__all__'

class AllPost(serializers.ModelSerializer):
    comments = AllComments(many=True, read_only=True)
    class Meta:
        model=Post
        fields='__all__'
        

    
