from django.contrib import admin
from users.models import Profile, User
from django.utils.html import format_html


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "fullname", "phone", "get_profile_name"]
    search_fields = ["email", "profile_owner__name", "fullname", "phone"]
    
    @admin.display(description="프로필 이름")
    def get_profile_name(self, obj):
        return obj.profile_owner.name
    
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "get_email", "name", "get_picture", "get_info"]
    search_fields = ["owner__email", "name"]
    
    @admin.display(description="사용자 이메일")
    def get_email(self, obj):
        return obj.owner.email
    
    @admin.display(description="프로필 사진")
    def get_picture(self, obj):
        if obj.picture:
            return format_html(f'<img src="{obj.picture.url}" alt="프로필 사진" style="width:30px; height:20px;">')
        else:
            return format_html(f'<img src="" alt="프로필 사진" style="width:30px; height:20px;">')
    
    @admin.display(description="프로필 소개")
    def get_info(self, obj):
        return obj.info[:30]