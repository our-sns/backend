from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email=email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="이메일 주소", max_length=100, unique=True)
    fullname = models.CharField(verbose_name="이름", max_length=20)
    password = models.CharField(verbose_name="비밀번호", max_length=300)
    phone = models.CharField(verbose_name="휴대폰", max_length=15, null=True)
    is_active = models.BooleanField(verbose_name="활성 여부", default=True)
    is_admin = models.BooleanField(verbose_name="관리자 여부", default=False)
    like_post = models.ManyToManyField("posts.Post", through='posts.Like', verbose_name="좋아요 누른 글", related_name="user_like_post")
    like_comment = models.ManyToManyField("comments.Comment", through='comments.CommentLike', verbose_name="좋아요 누른 댓글", related_name="user_like_comment")

    created_at = models.DateTimeField(verbose_name="가입일", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="프로필 갱신일", auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    objects = UserManager()

    def __str__(self):
        return self.email
 
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자 목록"

class Profile(models.Model):
    owner = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name="사용자 프로필", related_name="profile_owner")
    picture = models.ImageField(verbose_name="프로필 사진", null=True, blank=True, upload_to="profile/image/")
    name = models.CharField(verbose_name="프로필 이름", max_length=20, default="프로필 이름")
    info = models.TextField(verbose_name ="프로필 소개")
    
    def __str__(self):
        return f"{self.owner}의 프로필"
    
    class Meta:
        verbose_name = "사용자 프로필"
        verbose_name_plural = "사용자 프로필 목록"