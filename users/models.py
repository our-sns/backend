from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('Users must have an username')
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        email = self.normalize_email(email)
        user = self.model(
            username=username, email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username=username, email=email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user
    
# http://daplus.net/django-django-%EC%9D%B4%EB%A9%94%EC%9D%BC%EB%A1%9C-%EB%A1%9C%EA%B7%B8%EC%9D%B8/
# https://programmers-sosin.tistory.com/39
# https://wikidocs.net/10294
# https://developer-stories.tistory.com/17
# https://gigle.tistory.com/174
# https://iamthejiheee.tistory.com/78
# https://velog.io/@dev_dolxegod/Django-Authentication-System%EC%9D%98-%EB%AA%A8%EB%93%A0-%EA%B2%83-1-authuser-%EA%B8%B0%EB%B3%B8
class User(AbstractBaseUser):
    username = models.CharField(verbose_name="사용자 계정", max_length=20, unique=True)
    email = models.EmailField(verbose_name="이메일 주소", max_length=100)
    password = models.CharField(verbose_name="비밀번호", max_length=128)
    fullname = models.CharField(verbose_name="이름", max_length=20)
    profile = models.ImageField(
        verbose_name="프로필 사진", null=True, blank=True, upload_to="profile/image/"
    )
    is_active = models.BooleanField(verbose_name="활성 여부", default=True)
    is_admin = models.BooleanField(verbose_name="관리자 여부", default=False)

    created_at = models.DateTimeField(verbose_name="가입일", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="프로필 갱신일", auto_now=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "password"]

    objects = UserManager()

    def __str__(self):
        return self.username
 
 # https://www.hides.kr/942
 # https://dev-yakuza.posstree.com/ko/django/custom-user-model/
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
