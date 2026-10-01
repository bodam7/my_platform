from django.shortcuts import render
from .models import Category, JobPosting

def home(request):
    """
    메인 홈 화면 뷰
    - 업종 카테고리 목록 불러오기
    - 최신 구인 공고 목록 불러오기 (최신순 8개)
    """
    categories = Category.objects.all()
    recent_jobs = JobPosting.objects.filter(is_active=True).select_related('category').order_by('-created_at')[:8]
    
    context = {
        'categories': categories,
        'recent_jobs': recent_jobs,
    }
    # users 앱 안의 templates/users/home.html 경로를 바라보도록 설정
    return render(request, 'users/home.html', context)