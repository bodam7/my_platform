from django.contrib import admin
from .models import Category, JobPosting


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    업종 카테고리 관리자 설정
    - name: 업종명 (클릭 시 상세 이동)
    - order_num: 정렬 순서 (목록에서 숫자 직접 수정 가능)
    """
    list_display = ['name', 'order_num', 'slug', 'created_at']
    list_editable = ['order_num']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    """
    구인 공고 관리자 설정
    """
    list_display = ['title', 'company_name', 'category', 'is_urgent', 'is_closed', 'created_at']
    list_filter = ['category', 'is_urgent', 'is_closed']
    search_fields = ['title', 'company_name', 'location']
    list_editable = ['is_urgent', 'is_closed']