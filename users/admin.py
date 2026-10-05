from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import SiteConfig

User = get_user_model()

# 기존 사용자 모델 Admin 재등록 (에러 방지 처리)
if not admin.site.is_registered(User):
    admin.site.register(User, UserAdmin)

# 사이트 기본 설정 (로고 관리) Admin 등록
@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'updated_at')