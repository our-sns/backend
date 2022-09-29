from django.db import models
from users.models import User

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(to=User, verbose_name="작성자", on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(verbose_name="이미지", upload_to="attachment/image/")
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"게시글 : {self.title}"
    
    class Meta:
        verbose_name = "게시글"
        verbose_name_plural = "게시글 목록"