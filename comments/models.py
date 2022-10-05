from django.db import models
from posts.models import Post
from users.models import User

# Create your models here.
class Comment(models.Model):
    author = models.ForeignKey(to=User, verbose_name="작성자", on_delete=models.CASCADE, related_name="comments_author")
    post = models.ForeignKey(to=Post, verbose_name="게시글", on_delete=models.CASCADE, related_name="comments_post")
    content = models.TextField(verbose_name="댓글 내용")
    created_time = models.DateTimeField(verbose_name="댓글 생성일", auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name="댓글 갱신일", auto_now=True)

    def __str__(self):
<<<<<<< HEAD
        return f"{self.post}에 {self.author}이 작성한 댓글 : {self.content[:31] if len(self.content) >=30 else self.content}"
=======
        return f"{self.author}님이 작성한 {self.post}의 댓글"
>>>>>>> ccf5d822bfdc855db884126651814cdcfab04974
    
    class Meta:
        verbose_name = "댓글"
        verbose_name_plural = "댓글 목록"