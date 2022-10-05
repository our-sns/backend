from rest_framework import serializers
from .models import Post
from comments.serializers import CommentSerializer

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    comments_post = CommentSerializer(many=True, required=False)
    
    def get_author(self, obj):
        return obj.author.email
    
    def create(self, validated_data):
        user = self.context.get("request").user
        post = Post(**validated_data)
        post.author = user
        post.save()
        return post      
      
    class Meta:
        model = Post
<<<<<<< HEAD
        fields = ["id", "author", "content", "image", "created_at", "comments_post"]
=======
        fields = ["author", "content", "image", "created_at", "comments_post"]
>>>>>>> ccf5d822bfdc855db884126651814cdcfab04974
