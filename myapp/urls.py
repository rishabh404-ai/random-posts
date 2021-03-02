from django.urls import path
from rest_framework.routers import DefaultRouter

from myapp.views import RandomPostsViewSet

router = DefaultRouter()
router.register("random-posts", RandomPostsViewSet, basename="random-posts")


urlpatterns = [
                                                    
              ] + router.urls
