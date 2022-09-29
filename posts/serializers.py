from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    
    def get_author(self, obj):
        return obj.author.username
    
    def create(self, validated_data):
        user = self.context.get("request").user
        post = Post(**validated_data)
        post.author = user
        post.save()
        return post      
      
    class Meta:
        model = Post
        fields = ["author", "content", "image", "created_at", "comments_post"]