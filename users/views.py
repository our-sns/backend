from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from django.views.generic.base import TemplateView

from django.db.models import Q
from django.db.models.signals import post_save

from .models import Profile, User
from .permissions import CustomReadOnly
from posts.models import Post
from users.serializers import UserSignupSerializer, UserLoginSerializer, UserSerializer, ProfileSerializer

class UserSignupView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSignupSerializer
    
    def post(self, request):
        print(request.data)
        serialized_user_data = self.serializer_class(data=request.data)
        if serialized_user_data.is_valid():
            user = serialized_user_data.save()
            token = TokenObtainPairSerializer.get_token(user)
            access_token = str(token.access_token)
            return Response({
                "user": serialized_user_data.data,
                "message": "register success",
                "token": {"access": access_token}
                 }, status=status.HTTP_200_OK)
        return Response({"error": "에러가 발생하였습니다."}, status=status.HTTP_400_BAD_REQUEST)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)
            
class UserLoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    
    def post(self, request):
        user = authenticate(email=request.data.get("email"), password=request.data.get("password"))
 
        if user is not None:
            serialized_user_data = self.serializer_class(user)
            token = TokenObtainPairSerializer.get_token(user)
            access_token = str(token.access_token)
            return Response({
                "user": serialized_user_data.data,
                "message": "login success",
                "token": {"access": access_token}
                }, status=status.HTTP_200_OK)
        return Response({"error": "에러가 발생하였습니다."}, status=status.HTTP_400_BAD_REQUEST)
    
class UserSearchList(APIView):
    permission_classes = [CustomReadOnly]
    serializer_class = UserSerializer

    def get(self, request):
        search_keyword = request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        user_list = User.objects.order_by('-id')
        
        if search_keyword :
            if len(search_keyword) > 1 :
                if search_type == 'all':
                    search_user_list = user_list.filter(Q(email__icontains=search_keyword) | Q(fullname__icontains=search_keyword) | Q(profile_owner__name__icontains=search_keyword))
                elif search_type == 'email_profile':
                    search_user_list = user_list.filter(Q(email__icontains=search_keyword) | Q(profile_owner__name__icontains=search_keyword))
                elif search_type == 'email':
                    search_user_list = user_list.filter(email__icontains=search_keyword)
                elif search_type == 'fullname':
                    search_user_list = user_list.filter(fullname__icontains=search_keyword) 
                elif search_type == 'profile':
                    search_user_list = user_list.filter(profile_owner__name__icontains=search_keyword)

                if search_user_list:
                    serialized_search_user_list=self.serializer_class(search_user_list, many=True).data
                    return Response(serialized_search_user_list, status=status.HTTP_200_OK)
                else:
                    return Response({"message":"No post founding the query."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message":"Please enter at least 2 characters for the search term."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"Please enter a search term."}, status=status.HTTP_204_NO_CONTENT)

class MyInfo(APIView):
    permission_classes = [CustomReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = UserSerializer
    
    def get(self, request):
        email = request.user.email
        my_info = User.objects.get(email=email)
        serialized_my_info = self.serializer_class(my_info).data
        return Response(serialized_my_info, status=status.HTTP_200_OK)
    
    def put(self, request, **kwargs):
        id = request.user.id
        user = get_object_or_404(User, id=id)
        user_serializer = self.serializer_class(user, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
class MyProfile(APIView):
    permission_classes = [CustomReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = ProfileSerializer
    
    def get(self, request):
        id = request.user.id
        my_profile = get_object_or_404(Profile, owner=id)       
        serialized_my_profile = self.serializer_class(my_profile).data
        return Response(serialized_my_profile, status=status.HTTP_200_OK)
    
    def put(self, request, **kwargs):
        id = request.user.id
        profile = get_object_or_404(Profile, owner=id)
        profile_serializer = self.serializer_class(profile, data=request.data, partial=True)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# 메인 화면 접속
def index(request):
    # return redirect("login")
    return redirect("post_list")