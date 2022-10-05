from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
<<<<<<< HEAD
        return obj.author.email
=======
        return obj.author.username
>>>>>>> ccf5d822bfdc855db884126651814cdcfab04974

    def create(self, validated_data):
        user = self.context.get("request").user
        comment = Comment(**validated_data)
        comment.author = user
        comment.save()
        return comment

    class Meta:
        model = Comment
<<<<<<< HEAD
        fields = ["id", "content", "author", "post"]
=======
        fields = ["content", "author", "post"]
>>>>>>> ccf5d822bfdc855db884126651814cdcfab04974
        extra_kwargs = {'post': {'write_only': True}}
