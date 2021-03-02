import jwt
from django.contrib.auth.models import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import (DjangoUnicodeDecodeError, smart_bytes,
                                   smart_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
#from freelancer.serializers import RegisterSerializer

from rest_framework import exceptions, generics, permissions, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import User
from authentication.serializers import (RegisterSerializer, LoginSerializer, LogoutSerializer )
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser, FileUploadParser  



class RegisterViewSet(viewsets.ModelViewSet):
    """ View to register a User """

    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    http_method_names = ('post',)
    permission_classes = (permissions.AllowAny,)
  #  parser_classes = (FormParser,MultiPartParser) 
    
    def create(self, request, *args, **kwargs):
        serializer  = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid():
            self.perform_create(serializer)
            user_data = serializer.data
            user      = User.objects.get(email=user_data["email"])
            token   = RefreshToken.for_user(user).access_token
           
            return Response(
                    {
                      'status' : 'success',
                      'message': 'Registration Successful.',
                      'data' : serializer._data
                    }, status=status.HTTP_201_CREATED)

        else:
          raise ValidationError(
                      {
                        'status' : 'failed',
                        'message': serializer.errors,
                        'data' : []
                      })    
           
                   
    def perform_create(self, serializer):
        serializer.save()



    def perform_update(self, serializer):
        serializer.save()                
                  
     
class LoginViewSet(viewsets.ModelViewSet):
    """ View to login a User with username/email. """
    serializer_class = LoginSerializer
    queryset = User.objects.all()
    http_method_names = ('post',)
  #  parser_classes = (FormParser,MultiPartParser) 

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(
                      {
                        'status' : 'success',
                        'message': 'Login successful',
                        'data': serializer.data,

                      },status=status.HTTP_200_OK)
                      
        else:  
          raise ValidationError(
                          {
                            'status' : 'failed',
                            'message': serializer.errors,
                            'data': [] 
                          })    


class LogoutViewSet(viewsets.ModelViewSet):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ('post',)
  #  parser_classes = (FormParser,MultiPartParser) 

    def create(self, request,*args,**kwargs):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                    {
                        'status':'success',
                        'message':'Successfully logged out',
                    },status=status.HTTP_202_ACCEPTED)

        raise ValidationError ( 
                    {
                        'status' : 'failed',
                        'message': serializer.errors,
                        'data':[]
                    })      

