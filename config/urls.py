from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 기존에 만드셨던 관리자 주소
    path('ceo-master-room-8899/', admin.site.urls),
    
    # 회원가입, 로그인, 홈 등 users 앱의 모든 주소 연결
    path('', include('users.urls')),
]

# 개발 환경에서 업로드한 이미지(Media 파일) 접근 허용
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)