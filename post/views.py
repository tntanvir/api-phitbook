from django.shortcuts import render
from rest_framework import viewsets
from .models import Post,Comment,Likes
from .serializers import AllPost,AllComments,LikeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django. http import Http404 
from django.contrib.auth.models import User
# Create your views here.


class AllPostView(APIView):
    def get(self, request, format=None):
        user_id = request.query_params.get('user_id')
        username = request.query_params.get('username')
        # print('user_id: ', user_id)
        category = request.query_params.get('category')
        filter_image_null = request.query_params.get('image_null')
        filter_video_not_null = request.query_params.get('video_not_null')
        if user_id:
            posts = Post.objects.filter(user=user_id)
            print('user_id: ', user_id)
            print(posts)
            serializer = AllPost(posts, many=True)
            return Response(serializer.data)
        elif username:
            try:
                user_instance = User.objects.get(username=username)
                posts = Post.objects.filter(user=user_instance)
                serializer = AllPost(posts, many=True)  # Serialize the posts
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        elif category:
            posts = Post.objects.filter(category=category)
            serializer = AllPost(posts, many=True)
            return Response(serializer.data)
        else:
            posts = Post.objects.all()

            if filter_image_null and filter_video_not_null:
                posts = posts.filter(image__isnull=True).exclude(video__isnull=True)
            serializer = AllPost(posts, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
        print('inside post method')
        serializer = AllPost(data=request.data)
        serializer.user = request.user
        if serializer.is_valid():
            serializer.save(user = request.user)
        

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetailView(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = AllPost(post)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        print('inside put method')
        post = self.get_object(pk)
        serializer = AllPost(post, data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            print('VALIDATED')
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    



class AllCommentsView(APIView):
    serializer_class = AllComments
    def get(self, request, format=None):
        comment_id = request.query_params.get('comment_id')
        
        if comment_id:
            posts = Comment.objects.filter(id=comment_id)
            
            serializer = AllComments(posts, many=True)
            return Response(serializer.data)
       
        else:
            posts = Comment.objects.all()
            serializer = AllComments(posts, many=True)
            return Response(serializer.data)



    def post(self, request, format=None):
        serializer = AllComments(data=request.data)
        serializer.user = request.user
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, format=None):
        comment_id = request.data.get('id')
        if not comment_id:
            return Response({'error': 'Comment ID is required for updating'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AllComments(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            print("updated")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, format=None):
        comment_id = request.query_params.get('comment_id')
        if not comment_id:
            return Response({'error': 'Comment ID is required for deletion'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)







class LikeView(APIView):
    serializer_class = LikeSerializer

    def get(self, request, format=None):
        post_id = request.query_params.get('post_id')
        
        if post_id:
            likes = Likes.objects.filter(post=post_id)
            serializer = LikeSerializer(likes, many=True)
            return Response(serializer.data)
        else:
            likes = Likes.objects.all()
            serializer = LikeSerializer(likes, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
        user = request.user
        post_id = request.data.get('post')

        try:
            # Check if the like already exists
            like = Likes.objects.get(user=user, post=post_id)
            # If it exists, delete it (unlike)
            like.delete()
            return Response({'detail': 'Like removed'}, status=status.HTTP_204_NO_CONTENT)
        except Likes.DoesNotExist:
            # If it does not exist, create a new like (like)
            serializer = LikeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowingPostsAPIView(APIView):

    def get(self, request, format=None):
        user = request.user
        following_users = user.following.all().values_list('following', flat=True)
        posts = Post.objects.filter(user__in=following_users)
        serializer = AllPost(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)