from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import UserSignupView, UserLoginView, MyInfo, MyProfile, UserSearchList, index

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("", index, name="index"),
    path("signup/", UserSignupView.as_view(), name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path('search/', UserSearchList.as_view(), name="user_search"),
    path('my/info/', MyInfo.as_view()),
    path('my/profile/', MyProfile.as_view()),
]