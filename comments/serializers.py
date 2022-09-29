from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author.username

    def create(self, validated_data):
        user = self.context.get("request").user
        comment = Comment(**validated_data)
        comment.author = user
        comment.save()
        return comment

    class Meta:
        model = Comment
        fields = ["content", "author", "post"]
        extra_kwargs = {'post': {'write_only': True}}
