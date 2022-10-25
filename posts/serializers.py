from rest_framework import serializers

from users.models import Profile
from .models import Post, Image, Like
from comments.serializers import CommentSerializer

class ImageSerializer(serializers.ModelSerializer):
    
    def get_author(self, obj):
        return obj.author.email    

    def create(self, validated_data):
        user = self.context.get("request").user
        image = Image(**validated_data)
        image.author = user
        image.save()
        return image

    class Meta:
        model = Image
        fields = ["id", "photo", "post"]
        extra_kwargs = {'author': {'write_only': True}}
        
class LikeSerializer(serializers.ModelSerializer):
    post_author = serializers.SerializerMethodField()
    post_content = serializers.SerializerMethodField()
    
    def get_post_author(self, obj):
        profile_name = Profile.objects.filter(owner__id = obj.post.author.id).values("name").last()["name"]
        if profile_name:
            return profile_name
        else:
            return None
        
    def get_post_content(self, obj):
        content = obj.post.content[:30]
        return content

    def create(self, validated_data):
        user = self.context.get("request").user
        like = Like(**validated_data)
        like.user = user
        like.save()
        return like

    class Meta:
        model = Like
        fields = ["id", "post_id", "post_author", "post_content"]
    
class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    profile_name = serializers.SerializerMethodField()
    comments_post = CommentSerializer(many=True, required=False)
    images_post = ImageSerializer(many=True, required=False)
    like_user = serializers.SerializerMethodField()
    like_user_count = serializers.SerializerMethodField()
    
    def get_author(self, obj):
        return obj.author.email
    
    def get_profile_name(self, obj):
        profile_name = Profile.objects.filter(owner__id = obj.author.id).values("name").last()["name"]
        if profile_name:
            return profile_name
        else:
            return None
    
    def get_images_post(self, obj):
        image = obj.images.all()
        print(image)
        return image
    
    def get_like_user(self, obj):
        length = obj.like_user.count()
        like_user = []
        for i in range(length):
            email = obj.like_user.values('email')[i]['email']
            profile_name = Profile.objects.filter(owner__email=email).values('name').last()['name']
            like_user.append(profile_name)
        return like_user
    
    def get_like_user_count(self, obj):
        return obj.like_user.count()
    
    
    def create(self, validated_data):
        user = self.context.get("request").user
        post = Post(**validated_data)
        post.author = user
        post.save()
        return post      
      
    class Meta:
        model = Post
        fields = ["id", "author", "profile_name", "content", "created_at", "images_post", "comments_post", "like_user", "like_user_count"]