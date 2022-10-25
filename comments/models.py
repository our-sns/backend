from django.db import models
from posts.models import Post
from users.models import User

class Comment(models.Model):
    author = models.ForeignKey(to=User, verbose_name="작성자", on_delete=models.CASCADE, related_name="comments_author")
    post = models.ForeignKey(to=Post, verbose_name="게시글", on_delete=models.CASCADE, related_name="comments_post")
    content = models.TextField(verbose_name="댓글 내용")
    created_time = models.DateTimeField(verbose_name="댓글 생성일", auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name="댓글 갱신일", auto_now=True)
    comment_like_user = models.ManyToManyField("users.User", through='CommentLike', verbose_name="좋아요 누른 사람", related_name="comment_like_user")

    def __str__(self):
        return f'「{self.post}에 {self.author}이 작성한 댓글」 : "{self.content[:30] if len(self.content) >=30 else self.content}"'
    
    class Meta:
        verbose_name = "댓글"
        verbose_name_plural = "댓글 목록"
        
class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name="좋아요 누른 댓글", related_name="like_comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="좋아요 누른 사람", related_name="like_comment_user")
    
    def __str__(self):
        return f"{self.user}가 {self.comment}에 좋아요를 눌렀습니다."

    class Meta:
        verbose_name = "댓글 좋아요"
        verbose_name_plural = "댓글 좋아요 목록"