from rest_framework import serializers
from posts.models import Post
from users.models import Profile, User
from posts.serializers import PostSerializer

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, *args, **kwargs):
        user = super().create(*args, **kwargs)
        print("create")
        pw = user.password
        user.set_password(pw)
        user.save()
        return user
    
class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    def get_owner(self, obj):
        return obj.owner.email

    def create(self, validated_data):
        user = self.context.get("request").user
        profile = Profile(**validated_data)
        profile.owner = user
        profile.save()
        return profile

    class Meta:
        model = Profile
        fields = ["id", "owner", "picture", "name", "info"]
        extra_kwargs = {'owner': {'write_only': True}}
        
class UserSerializer(serializers.ModelSerializer):
    profile_name = serializers.SerializerMethodField()
    like_post = serializers.SerializerMethodField()
    like_post_count = serializers.SerializerMethodField()
    like_comment = serializers.SerializerMethodField()
    like_comment_count = serializers.SerializerMethodField()
    
    def get_profile_name(self, obj):
        profile_name = Profile.objects.filter(owner__id = obj.id).values("name").last()["name"]
        if profile_name:
            return profile_name
        else:
            return None
    
    def get_like_post(self, obj):
        return obj.like_post.values('content')[:30]
    
    def get_like_post_count(self, obj):
        return obj.like_post.count()
    
    def get_like_comment(self, obj):
        return obj.like_comment.values('content')[:30]
    
    def get_like_comment_count(self, obj):
        return obj.like_comment.count()
    
    class Meta:
        model = User
        fields = ["id", "email", "profile_name", "fullname", "phone", "like_post", "like_post_count", "like_comment", "like_comment_count"]
        
class UserLoginSerializer(serializers.ModelSerializer):
    profile_name = serializers.SerializerMethodField()
    
    def get_profile_name(self, obj):
        profile_name = Profile.objects.filter(owner__id = obj.id).values("name").last()["name"]
        if profile_name:
            return profile_name
        else:
            return None
    
    class Meta:
        model = User
        fields = ["id", "email", "profile_name"]
