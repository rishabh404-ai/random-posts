from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import EmailValidator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from authentication.models import User


class RegisterSerializer(serializers.ModelSerializer):
    
    firstname             = serializers.CharField(write_only=True,required=False,max_length=255)   
    lastname              = serializers.CharField(write_only=True,required=False,max_length=255)        
    email                 = serializers.EmailField(required=True)
    password              = serializers.CharField(max_length=68, min_length=2, write_only=True,required=True,style={'input_type':'password'})
    password_confirmation = serializers.CharField(max_length=68,min_length=2,write_only=True,required=True,style={'input_type':'password'})
    username              = serializers.CharField(required=True)
    is_verified           = serializers.BooleanField(read_only=True) 
    is_active             = serializers.BooleanField(read_only=True) 

    class Meta:
        model  = User
        fields = [
            "id",
            "email",
            "username",
            "full_name",
            "password",
            'password_confirmation',
            "is_verified",
            "is_active",
            "firstname",
            "lastname",

        ]
              

    def validate(self, data):

        email                 = data.get("email",'')
        password              = data.get("password",'')
        password_confirmation = data.get('password_confirmation','')
        username              = data.get("username",'')
        user_type             = data.get("user_type",'')
 

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'This email is already taken'})

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': 'This username is already taken'})

        if not email:
            raise serializers.ValidationError({'email': 'Please enter your Email-ID'})
        
        if not username:
            raise serializers.ValidationError({'username': 'Please enter valid username'})

        if not username.isalnum():
            raise serializers.ValidationError({'username': 'The username should only contain alphanumeric characters'})                                             
                                                        
        if not password:
            raise serializers.ValidationError({'password': 'Please enter valid password'})   

        if not password_confirmation:
            raise serializers.ValidationError({'password_confirmation': 'Passwords are not matching'})   
       
        if password != password_confirmation:
            raise serializers.ValidationError({'passwords': 'Passwords are not matching'})

        return data
   

    def create(self, validated_data):
        firstname  = validated_data.get('firstname')
        lastname   = validated_data.get('lastname')
        email      = validated_data.get('email',)
        username   = validated_data.get('username',)
        password   = validated_data.get('password',)

        try:
            user = User.objects.create_user(
                firstname=firstname,lastname=lastname,email=email,username=username,password=password) 
                
            user.save()
            return user

        except Exception as e:
            return e    

    def update(self,instance,validated_data):
        instance.firstname  = validated_data.get('firstname', instance.firstname)
        instance.lastname   = validated_data.get('lastname',instance.lastname)
        instance.save()

        return instance       



class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=255, min_length=3, read_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    email_or_username = serializers.CharField(max_length=255, min_length=3, write_only=True,required=True)
    password          = serializers.CharField(max_length=68, min_length=2, write_only=True,style={'input_type':'password'},required=True)
    tokens            = serializers.CharField(max_length=68, min_length=6, read_only=True)
    
    def validate(self, attrs):
        email_or_username = attrs.get("email_or_username", "")
        password          = attrs.get("password", "")
        if User.objects.filter(email=email_or_username).exists() or User.objects.filter(username=email_or_username).exists():
            user_obj          = User.objects.filter(email=email_or_username).first() or User.objects.filter(username=email_or_username).first()
            email             = attrs.get("email")
        else:
            raise serializers.ValidationError({'email_or_username':'Entered email/username does not exists.'})
       
       
        user = auth.authenticate(email=user_obj.email, password=password)
        
        if not user:
            raise serializers.ValidationError({'email_or_username':"Invalid Credentials, Try again"})

        if not email_or_username:
            raise serializers.ValidationError({'email_or_username':'Please enter a valid email or username'})

        if not password:
            raise serializers.ValidationError({'password':'Please enter password'})

       
        return {
            "email": user.email,
            "username": user.username,
            "tokens": user.tokens}


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            raise serializers.ValidationError({'status' : 'failed',
                                               'token':'bad_token'})




