from rest_framework import serializers
from .models import Comment, CommentLike
from users.models import Profile

class CommentLikeSerializer(serializers.ModelSerializer):
    comment_author = serializers.SerializerMethodField()
    comment_content = serializers.SerializerMethodField()
    
    def get_comment_author(self, obj):
        profile_name = Profile.objects.filter(owner__id = obj.comment.author.id).values("name").last()["name"]
        if profile_name:
            return profile_name
        else:
            return obj.comment.author.email
        
    def get_comment_content(self, obj):
        content = obj.comment.content
        return content

    def create(self, validated_data):
        user = self.context.get("request").user
        like = CommentLike(**validated_data)
        like.user = user
        like.save()
        return like

    class Meta:
        model = CommentLike
        fields = ["id", "comment_id", "comment_author", "comment_content"]
        extra_kwargs = {"comment_content" : {'write_only': True}}


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    comment_like_user = serializers.SerializerMethodField()
    comment_like_user_count = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author.email

    def create(self, validated_data):
        user = self.context.get("request").user
        comment = Comment(**validated_data)
        comment.author = user
        comment.save()
        return comment
    
    def get_comment_like_user(self, obj):
        length = obj.comment_like_user.count()
        comment_like_user = []
        for i in range(length):
            email = obj.comment_like_user.values('email')[i]['email']
            profile_name = Profile.objects.filter(owner__email=email).values('name').last()['name']
            comment_like_user.append(profile_name)
        return comment_like_user
    
    def get_comment_like_user_count(self, obj):
        return obj.comment_like_user.count()

    class Meta:
        model = Comment
        fields = ["id", "post_id", "author", "content", "comment_like_user", "comment_like_user_count"]
        extra_kwargs = {'post': {'write_only': True}}


