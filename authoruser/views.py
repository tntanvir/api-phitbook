from django.shortcuts import render
from .serializers import UserRegister,loginSerializer,Alluser,MainUser
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import login,logout,authenticate
from .models import UserModel

from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework import viewsets,filters
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
            confirm_link=f"http://127.0.0.1:8000/authore/active/{uid}/{token}/"
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
                return Response({'token':token.key,'id':user.id})
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
        if user_id:
            try:
                user = UserModel.objects.get(user=user_id)
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

class MainUserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class=MainUser





    