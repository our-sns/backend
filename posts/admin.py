from django.contrib import admin
from posts.models import Image, Post, Like
from django.utils.html import format_html

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "get_email", "get_profile_name", "get_content", "get_photo"]
    
    @admin.display(description="작성자 이메일")
    def get_email(self, obj):
        return obj.author.email
    
    @admin.display(description="작성자 프로필 이름")
    def get_profile_name(self, obj):
        return obj.author.profile_owner.name
    
    @admin.display(description="게시글 내용")
    def get_content(self, obj):
        return obj.content[:30]
    
    @admin.display(description="게시글 이미지")
    def get_photo(self, obj):
        post=Post.objects.get(id=obj.id).images_post.first()
        if post:
            return format_html(f'<img src="{post.photo.url}", style="width:30px; height:20px;">')
        else:
            return format_html(f'<img src="" alt="게시글 이미지" style="width:30px; height:20px;">')
    
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["id", "get_email", "get_content", "get_photo"]
    
    @admin.display(description="작성자 이메일")
    def get_email(self, obj):
        return obj.author.email
    
    @admin.display(description="게시글 내용")
    def get_content(self, obj):
        return obj.post.content[:30]
    
    @admin.display(description="게시글 이미지")
    def get_photo(self, obj):
        print(obj.photo.url)
        return format_html(f'<img src="{obj.photo.url}" style="width:30px; height:20px;">')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ["id", "post", "user"]