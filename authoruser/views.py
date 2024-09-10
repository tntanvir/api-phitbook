from django.shortcuts import render
from .serializers import UserRegister,loginSerializer,Alluser,MainUser,FollowSerializer,FollowersSerializer,FollowingSerializer
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import login,logout,authenticate
from .models import UserModel,Follow

from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework import viewsets,filters
from django.shortcuts import get_object_or_404
# email
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
# Create your views here.

class PatientRegistration(APIView):
    serializer_class = UserRegister
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            token=default_token_generator.make_token(user)
            print('token: ',token)
            uid= urlsafe_base64_encode(force_bytes(user.pk))
            print('uid: ',uid)
            confirm_link=f"https://api-phitbook.onrender.com/authore/active/{uid}/{token}/"
            print('confirm link: ',confirm_link)
            
            email_subject='Confirm Your Account'
            email_body=render_to_string('confirm_email.html',{'confirm_link':confirm_link})

            email=EmailMultiAlternatives(email_subject,'',to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()

            return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

def activate(request,uid64,token):
    try:
        uid=urlsafe_base64_decode(uid64).decode()
        user=User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active=True
        user.save()
        return redirect('registar')
    else:
        return redirect('registar')
    


class UserLogin(APIView):
    def post(self,request):
        serializer=loginSerializer(data=self.request.data)
        if serializer.is_valid():
            username=serializer.validated_data["username"]
            password=serializer.validated_data["password"]

            user=authenticate(username=username,password=password)

            if user:
                token,_=Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({'token':token.key,'id':user.id,'user':user.username})
            else:
                return Response('Invalid credentials',status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors)

class Userlogout(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')
    

class AllUserView(APIView):
    serializer_class = Alluser
    def get(self, request):
        user_id = request.query_params.get('user_id')
        username = request.query_params.get('username')
        if user_id:
            try:
                user = UserModel.objects.get(user=user_id)
                serializer = Alluser(user)
            except UserModel.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        elif username:
            try:
                user_instance = User.objects.get(username=username)
                user = UserModel.objects.get(user=user_instance)
                serializer = Alluser(user)
            except UserModel.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            users = UserModel.objects.all()
            serializer = Alluser(users, many=True)
        
        return Response(serializer.data)
    def put(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "User ID is required to update data"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = UserModel.objects.get(user=user_id)
        except UserModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = Alluser(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class MainUserView(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class=MainUser


class MainUserView(APIView):
    def get(self, request, pk=None):
        username = request.query_params.get('username')
        if pk:
            user = get_object_or_404(User, pk=pk)
            serializer = MainUser(user)
        elif username:
            user = get_object_or_404(User, username=username)
            serializer = MainUser(user)
        else:
            users = User.objects.all()
            serializer = MainUser(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MainUser(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = MainUser(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class FollowUserView(APIView):
    def post(self, request, username):
        try:
            # Get the user to be followed
            user_to_follow = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get the current logged-in user
        current_user = request.user
        
        # Check if the current user is already following the target user
        follow_obj, created = Follow.objects.get_or_create(follower=current_user, following=user_to_follow)

        if created:
            # If the follow relationship was created, return a success message
            return Response(
                {'message': f'You have successfully followed {user_to_follow.username}!'},
                status=status.HTTP_201_CREATED
            )
        else:
            # If the follow relationship already exists, unfollow the user and return a message
            follow_obj.delete()
            return Response(
                {'message': f'You have successfully unfollowed {user_to_follow.username}.'},
                status=status.HTTP_200_OK
            )
class FollowersView(APIView):
    def get(self, request, username):
        # Get the user whose followers you want to retrieve by username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get all users who follow the target user
        followers = Follow.objects.filter(following=user)
        serializer = FollowersSerializer(followers, many=True)
        return Response(serializer.data)

class FollowingView(APIView):
    def get(self, request, username):
        # Get the user whose following list you want to retrieve by username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get all users the target user is following
        following = Follow.objects.filter(follower=user)
        serializer = FollowingSerializer(following, many=True)
        return Response(serializer.data)
    

class FollowStatusAPIView(APIView):


    def get(self, request, username):
        try:
            target_user = User.objects.get(username=username)
            is_following = Follow.objects.filter(follower=request.user, following=target_user).exists()
            return Response({'is_following': is_following}, status=200)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)