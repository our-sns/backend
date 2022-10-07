from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import UserLoginSerializer, UserSignupSerializer
from django.contrib.auth import authenticate
from django.shortcuts import redirect


# https://hyeo-noo.tistory.com/302
class UserSignupView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSignupSerializer
    
    def post(self, request):
        serialized_user_data = self.serializer_class(data=request.data)
        if serialized_user_data.is_valid():
            user = serialized_user_data.save()
            token = TokenObtainPairSerializer.get_token(user)
            access_token = str(token.access_token)
            return Response({
                "user": serialized_user_data.data,
                "message": "register success",
                "token": {"access": access_token} # refresh token은 백엔드에서만 볼 수 있게끔 작업함. 바로 쿠키셋 하면서 프론트로 전달 / 실제로는 access_token만 넘긴다 → 무슨말?
                 }, status=status.HTTP_200_OK)
        return Response({"error": "에러가 발생하였습니다."}, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    
    def post(self, request):
        # user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
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
    
# 로그아웃 
# https://medium.com/@yunusemrecevik
# https://medium.com/django-rest/logout-django-rest-framework-eb1b53ac6d35
# https://medium.com/@pcj0198
# https://medium.com/chanjongs-programming-diary/django-rest-framework-drf-환경에서-jwt-기반-authentication-세팅하기-with-simplejwt-blacklist-기법으로-보안-7db20665ee78
# https://donis-note.medium.com/django-rest-framework-authentication-permission-%EC%9D%B8%EC%A6%9D%EA%B3%BC-%EA%B6%8C%ED%95%9C-cc9b183fd901
# https://newbiecs.tistory.com/267
# https://jaeseo0519.tistory.com/76

# 액세스토큰을 response의 body(열어볼수 있음)에 포함시켜서 프론트에 보내고, 리프레쉬토큰을 response의 쿠키(암호화처리)에 포함시켜서 프론트에 보냄.
# 로그아웃 구현은 일단 보류
class UserLogoutView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]   # body에서 데이터를 가져와라
            print(refresh_token)
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
# 메인 화면 접속
def index(request):
    return redirect("login")

