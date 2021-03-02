from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.views import LoginViewSet, LogoutViewSet, RegisterViewSet

router = DefaultRouter()
router.register("register", RegisterViewSet, basename="register")
router.register("login",    LoginViewSet,    basename="login")
router.register("logout",   LogoutViewSet,   basename="logout")

urlpatterns = [

                  path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
                                                     
              ] + router.urls


