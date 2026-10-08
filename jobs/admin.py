from django.contrib import admin
from .models import Category, JobPosting, Application


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """업종 카테고리 관리자 설정"""
    list_display = ['id', 'name', 'order', 'image', 'slug']
    list_editable = ['order']  # 목록 화면에서 순서를 바로 수정 가능
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    ordering = ('order', 'id')


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    """구인 공고 관리자 설정 (10초 빠른 업로드 동선 최적화)"""
    list_display = ['title', 'category', 'priority_order', 'is_urgent', 'is_vip', 'is_closed', 'created_at']
    list_editable = ['priority_order', 'is_urgent', 'is_vip', 'is_closed']  # 목록에서 즉시 상태 변경
    list_filter = ['category', 'is_urgent', 'is_vip', 'is_closed']
    search_fields = ['title', 'company_name', 'location']
    ordering = ('-priority_order', '-created_at')
    
    # 10초 빠른 업로드 동선: 기본 정보(제목/이미지/유튜브) 우선 배치, 상세 정보는 기본 접음
    fieldsets = (
        ('기본 정보 (빠른 업로드)', {
            'fields': ('category', 'title', 'image', 'youtube_url')
        }),
        ('노출 및 상태 설정', {
            'fields': ('priority_order', 'is_urgent', 'is_closed', 'is_vip')
        }),
        ('추가 상세 정보 (선택 사항)', {
            'classes': ('collapse',),  # 접힘 상태
            'fields': ('company_name', 'location', 'pay', 'description')
        }),
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """즉시 지원 내역 관리자 설정 (지원자 정보 확인)"""
    list_display = ['name', 'phone_number', 'job_posting', 'applied_at']
    list_filter = ['job_posting__category', 'applied_at']
    search_fields = ['name', 'phone_number', 'job_posting__title']
    readonly_fields = ['name', 'phone_number', 'job_posting', 'applied_at']