from django.shortcuts import get_object_or_404
from .serializers import PostSerializer
from .models import Post
from .permissions import CustomReadOnly
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.
class PostList(APIView):
    permission_classes = [CustomReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = PostSerializer

    def get(self, request):
        post = Post.objects.all()
        serialized_post_data = self.serializer_class(post, many=True).data
        return Response(serialized_post_data, status=status.HTTP_200_OK)

    def post(self, request):
        post_serializer = self.serializer_class(data=request.data, context={'request': request})
        if post_serializer.is_valid():
            post_serializer.save()
            return Response({"message": "정상"}, status=status.HTTP_200_OK)
        return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):
    permission_classes = [CustomReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = PostSerializer

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serialized_post_data = self.serializer_class(post).data
        return Response(serialized_post_data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(self.request, post)
        post_serializer = self.serializer_class(post, data=request.data)
        if post_serializer.is_valid():
            post_serializer.save()
            return Response(post_serializer.data)
        return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(self.request, post)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)