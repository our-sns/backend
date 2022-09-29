from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import UserSerializer, UserSignupSerializer
from django.contrib.auth import authenticate


# https://hyeo-noo.tistory.com/302
class UserSignupView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSignupSerializer
    
    def post(self, request):
        serialized_user_data = self.serializer_class(data=request.data)
        if serialized_user_data.is_valid():
            user = serialized_user_data.save()
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            return Response({
                "user": serialized_user_data.data,
                "message": "register success",
                "token": {"access": access_token, "refresh": refresh_token} # refresh token은 백엔드에서만 볼 수 있게끔 작업함. 바로 쿠키셋 하면서 프론트로 전달 / 실제로는 access_token만 넘긴다 → 무슨말?
                 }, status=status.HTTP_200_OK)
        return Response({"error": "에러가 발생하였습니다."}, status=status.HTTP_400_BAD_REQUEST)
    
class UserView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    
    def post(self, request):
        user = authenticate(email=request.data.get("email", password=request.data.get("password")))
        if user is not None:
            serialized_user_data = self.serializer_class(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            return Response({
                "user": serialized_user_data.data,
                "message": "login success",
                "token": {"access": access_token, "refresh": refresh_token}
                }, status=status.HTTP_200_OK)
        return Response({"error": "에러가 발생하였습니다."}, status=status.HTTP_400_BAD_REQUEST)
    
# 로그아웃 
# https://medium.com/django-rest/logout-django-rest-framework-eb1b53ac6d35
# https://donis-note.medium.com/django-rest-framework-authentication-permission-%EC%9D%B8%EC%A6%9D%EA%B3%BC-%EA%B6%8C%ED%95%9C-cc9b183fd901
class LogoutView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)