
from rest_framework import serializers
from .models import UserModel,Follow
from django.contrib.auth.models import User
     

class UserRegister(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=True)
    location = serializers.CharField(required=True)
    image=serializers.URLField(required=True)
    confirm_password = serializers.CharField(required =True)

    
    class Meta:
        model = User
        fields = ['image','username','first_name','last_name','email','phone_number','location', 'password','confirm_password']

    def save(self):
        image = self.validated_data.get('image',None)
        username=self.validated_data['username']
        email=self.validated_data['email']
        first_name=self.validated_data['first_name']
        last_name=self.validated_data['last_name']
        phone_number=self.validated_data['phone_number']
        location=self.validated_data['location']
        password=self.validated_data['password']
        confirm_password=self.validated_data['confirm_password']
        
        if password!=confirm_password:
            raise serializers.ValidationError({'password':'Passwords do not match'})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email':'Email already exists'})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username':'Username already exists'})
        account=User(username=username, email=email,first_name=first_name,last_name=last_name)
        
        account.set_password(password)
        account.is_active=False
        account.save()
        userAccount=UserModel(
            user=account,
            image=image,
            phone_number=phone_number,
            location=location,
            )
        userAccount.save()

        return account
    

class loginSerializer(serializers.Serializer):
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True)


class Alluser(serializers.ModelSerializer):
    # id=serializers.StringRelatedField(many=False)
    class Meta:
        model=UserModel
        fields='__all__'


class MainUser(serializers.ModelSerializer):
    # user=serializers.StringRelatedField(many=False)
    class Meta:
        model=User
        fields = ['id','username','first_name','last_name','email']
        






class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ['follower', 'following', 'created_at']

    def get_follower(self, obj):
        # Merge MainUser and Alluser data into a single dictionary
        main_user_data = MainUser(obj.follower).data
        all_user_data = Alluser(obj.follower.usermodel).data
        return {**main_user_data, **all_user_data}

    def get_following(self, obj):
        # Merge MainUser and Alluser data into a single dictionary
        main_user_data = MainUser(obj.following).data
        all_user_data = Alluser(obj.following.usermodel).data
        return {**main_user_data, **all_user_data}

class FollowersSerializer(serializers.ModelSerializer):
    follower = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ['follower', 'created_at']

    def get_follower(self, obj):
        main_user_data = MainUser(obj.follower).data
        all_user_data = Alluser(obj.follower.usermodel).data
        return {**main_user_data, **all_user_data}

class FollowingSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ['following', 'created_at']

    def get_following(self, obj):
        # Merge MainUser and Alluser data into a single dictionary
        main_user_data = MainUser(obj.following).data
        all_user_data = Alluser(obj.following.usermodel).data
        return {**main_user_data, **all_user_data}