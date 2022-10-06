from django.db import models
from users.models import User

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(to=User, verbose_name="작성자", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(verbose_name="게시글 내용")
    image = models.ImageField(verbose_name="게시글 이미지", upload_to="attachment/image/")
    created_at = models.DateTimeField(verbose_name="게시글 생성일", auto_now_add=True, null=True)
    updated_at = models.DateTimeField(verbose_name="게시글 갱신일", auto_now=True)
    
    def __str__(self):
        return f"{self.author}의 게시글"

    
    class Meta:
        verbose_name = "게시글"
        verbose_name_plural = "게시글 목록"