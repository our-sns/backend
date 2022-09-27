from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("Users must have an username")
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username=username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(verbose_name="사용자 계정", max_length=20, unique=True)
    email = models.EmailField(verbose_name="이메일 주소, max_length=100")
    password = models.CharField(verbose_name="비밀번호", max_length=128)
    fullname = models.CharField(verbose_name="이름", max_length=20)
    join_date = models.DateTimeField(verbose_name="가입일", auto_now_add=True)
    is_active = models.BooleanField(verbose_name="활성 여부", default=True)
    is_admin = models.BooleanField(verbose_name="관리자 여부", default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자 목록"
