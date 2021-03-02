from rest_framework import serializers
from myapp.models import RandomPosts


class RandomPostsSerializer(serializers.ModelSerializer):

    class Meta:
        model  = RandomPosts
        fields = ['user_id',
                  'id',
                  'title',
                  'body']