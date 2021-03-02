from django.shortcuts import render
from myapp.models import RandomPosts
from myapp.serializers import RandomPostsSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser, FileUploadParser 

# Create your views here.

class RandomPostsViewSet(viewsets.ModelViewSet):
    queryset         = RandomPosts.objects.all()
    serializer_class = RandomPostsSerializer
#    parser_classes = (FormParser,MultiPartParser)    
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