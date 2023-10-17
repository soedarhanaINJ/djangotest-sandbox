from django.urls import path
from rest_framework_simplejwt.views import (TokenBlacklistView,
                                            TokenObtainPairView,
                                            TokenRefreshView)

urlpatterns = [
    path("login/", TokenObtainPairView.as_view()),
    path("logout/", TokenBlacklistView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
]
