from django.contrib import admin
from .models import Category, JobPosting


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'order', 'image', 'slug']
    list_editable = ['order']
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