from django.shortcuts import get_object_or_404
from .serializers import CommentSerializer, CommentLikeSerializer
from .models import Comment, CommentLike
from posts.models import Post
from comments.permissions import CustomReadOnly
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.
class CommentList(APIView):
    permission_classes = [CustomReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = CommentSerializer

    def get(self, request):
        postId = request.GET.get('postId')
        post = get_object_or_404(Post, pk=postId)
        comment = Comment.objects.filter(post=post)
        serialized_comment_data = self.serializer_class(comment, many=True).data
        return Response(serialized_comment_data, status=status.HTTP_200_OK)

    def post(self, request):
        comment_serializer = self.serializer_class(data=request.data, context={'request': request})
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response({"message": "정상"}, status=status.HTTP_200_OK)
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetail(APIView):
    permission_classes = [CustomReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = CommentSerializer

    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serialized_comment_data = self.serializer_class(comment).data
        return Response(serialized_comment_data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(self.request, comment)
        comment_serializer = self.serializer_class(comment, data=request.data, partial=True)
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data)
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(self.request, comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CommentLikeList(APIView):
    permission_classes = [CustomReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = CommentLikeSerializer
    
    def get(self, request):
        id = request.user.id
        comment_like = CommentLike.objects.filter(user=id)
        serialized_comment_like_data = self.serializer_class(comment_like, many=True).data
        return Response(serialized_comment_like_data, status=status.HTTP_200_OK)

    def post(self, request):
        commentId = request.GET.get('commentId')
        comment = get_object_or_404(Comment, pk=commentId)
        if request.user in comment.comment_like_user.all():
            comment.comment_like_user.remove(request.user)
            return Response({'message':'Like cancelled.'}, status=status.HTTP_200_OK)
        else: 
            comment.comment_like_user.add(request.user)
            return Response({'message': 'Comment liked.'}, status=status.HTTP_200_OK)
