from django.shortcuts import render
from rest_framework import permissions, status, viewsets
from rest_framework.parsers import (FileUploadParser, FormParser, JSONParser,
                                    MultiPartParser)
from rest_framework.response import Response

from myapp.models import RandomPosts
from myapp.serializers import RandomPostsSerializer

# Create your views here.

class RandomPostsViewSet(viewsets.ModelViewSet):
    queryset           = RandomPosts.objects.all()
    serializer_class   = RandomPostsSerializer
    parser_classes     = (FormParser,MultiPartParser)    
    permission_classes = (permissions.IsAuthenticated,)    

    def create(self,request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)     
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers    = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
   
    def perform_create(self, serializer):
        serializer.save()     

    def perform_update(self, serializer):
        serializer.save()       
