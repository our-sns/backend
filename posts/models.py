from django.db import models
from users.models import User

class Post(models.Model):
    author = models.ForeignKey(to=User, verbose_name="작성자", on_delete=models.CASCADE, related_name="post_author")
    content = models.TextField(verbose_name="게시글 내용")
    created_at = models.DateTimeField(verbose_name="게시글 생성일", auto_now_add=True, null=True)
    updated_at = models.DateTimeField(verbose_name="게시글 갱신일", auto_now=True)
    like_user = models.ManyToManyField("users.User", through='Like', verbose_name="좋아요 누른 사람", related_name="post_like_user")
    
    def __str__(self):
        return f"[{self.id} : {self.author}의 게시글]"
  
    class Meta:
        verbose_name = "게시글"
        verbose_name_plural = "게시글 목록"
        
class Image(models.Model):
    author = models.ForeignKey(to=User, verbose_name="작성자", on_delete=models.CASCADE, related_name="images_author")
    post = models.ForeignKey(to=Post, verbose_name="게시글", on_delete=models.CASCADE, related_name="images_post")
    photo = models.ImageField(verbose_name="게시글 이미지", upload_to="attachment/image/")
    
    def __str__(self):
        return f"{self.post}에 {self.author}가 업로드한 사진"

    class Meta:
        verbose_name = "사진"
        verbose_name_plural = "사진 목록"
        
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="좋아요 누른 글", related_name="like_post")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="좋아요 누른 사람", related_name="like_user")
    
    def __str__(self):
        return f"{self.user}가 {self.post}에 좋아요를 눌렀습니다."
    
    class Meta:
        verbose_name = "게시글 좋아요"
        verbose_name_plural = "게시글 좋아요 목록"