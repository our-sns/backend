from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import UserSignupView, UserView, LogoutView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/signup/", UserSignupView.as_view()),
    path("api/auth/", UserView.as_view()),
    path("api/auth/logout/", LogoutView.as_view()),
]