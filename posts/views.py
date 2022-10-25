from django.shortcuts import get_object_or_404
from .serializers import PostSerializer, ImageSerializer, LikeSerializer
from .models import Post, Image, Like
from users.models import Profile, User
from .permissions import CustomReadOnly
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q

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
   
class ImageList(APIView):
    permission_classes = [CustomReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = ImageSerializer

    def get(self, request):
        postId = request.GET.get('postId')
        print(postId)
        post = get_object_or_404(Post, pk=postId)
        image = Image.objects.filter(post=post)
        serialized_image_data = self.serializer_class(image, many=True).data
        return Response(serialized_image_data, status=status.HTTP_200_OK)

    def post(self, request):
        image_serializer = self.serializer_class(data=request.data, context={'request': request})
        if image_serializer.is_valid():
            image_serializer.save()
            return Response({"message": "정상"}, status=status.HTTP_200_OK)
        return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImageDetail(APIView):
    permission_classes = [CustomReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = ImageSerializer

    def get(self, request, pk):
        postId = request.GET.get('postId')
        image = Image.objects.filter(post_id=postId, pk=pk)
        if image:
            serialized_image_data = self.serializer_class(image, many=True).data
            return Response(serialized_image_data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        image = get_object_or_404(Image, pk=pk)
        self.check_object_permissions(self.request, image)
        image_serializer = self.serializer_class(image, data=request.data, partial=True)
        if image_serializer.is_valid():
            image_serializer.save()
            return Response(image_serializer.data)
        return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        image = get_object_or_404(Image, pk=pk)
        self.check_object_permissions(self.request, image)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class LikeList(APIView):
    permission_classes = [CustomReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = LikeSerializer
    
    def get(self, request):
        id = request.user.id
        like = Like.objects.filter(user=id)
        serialized_like_data = self.serializer_class(like, many=True).data
        return Response(serialized_like_data, status=status.HTTP_200_OK)

    def post(self, request):
        postId = request.GET.get('postId')
        post = get_object_or_404(Post, pk=postId)
        if request.user in post.like_user.all():
            post.like_user.remove(request.user)
            return Response({'message':'Like cancelled.'}, status=status.HTTP_200_OK)
        else: 
            post.like_user.add(request.user)
            return Response({'message': 'Post liked.'}, status=status.HTTP_200_OK)
        
        
class PostSearchList(APIView):
    permission_classes = [CustomReadOnly]
    serializer_class = PostSerializer

    def get(self, request):
        search_keyword = request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        post_list = Post.objects.order_by('-id')
        if search_keyword :
            if len(search_keyword) > 1 :
                if search_type == 'all':
                    search_post_list = post_list.filter(Q(content__icontains=search_keyword) | Q(author__email__icontains=search_keyword) | Q(author__profile_owner__name__icontains=search_keyword))
                elif search_type == 'email_name':
                    search_post_list = post_list.filter(Q(author__email__icontains=search_keyword) | Q(author__profile_owner__name__icontains=search_keyword))
                elif search_type == 'content':
                    search_post_list = post_list.filter(content__icontains=search_keyword)
                elif search_type == 'email':
                    search_post_list = post_list.filter(author__email__icontains=search_keyword) 
                elif search_type == 'name':
                    search_post_list = post_list.filter(author__profile_owner__name__icontains=search_keyword)

                if search_post_list:
                    serialized_search_post_list=self.serializer_class(search_post_list, many=True).data
                    return Response(serialized_search_post_list, status=status.HTTP_200_OK)
                else:
                    return Response({"message":"No post founding the query."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message":"Please enter at least 2 characters for the search term."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"Please enter a search term."}, status=status.HTTP_204_NO_CONTENT)
