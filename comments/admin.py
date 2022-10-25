from django.contrib import admin
from comments.models import Comment, CommentLike

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "get_post_email", "get_post", "get_comment_email", "get_comment"]
    
    @admin.display(description="게시글 작성자")
    def get_post_email(self, obj):
        return obj.post.author.email
    
    @admin.display(description="게시글 내용")
    def get_post(self, obj):
        return obj.post.content[:30]
    
    @admin.display(description="댓글 작성자")
    def get_comment_email(self, obj):
        return obj.author.email
    
    @admin.display(description="댓글 내용")
    def get_comment(self, obj):
        return obj.content[:30]
    
@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ["id", "comment", "user"]