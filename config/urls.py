from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 기존에 만드셨던 관리자 주소 (이게 그대로 들어있어서 안 날아갑니다!)
    path('ceo-master-room-8899/', admin.site.urls),
    
    # 회원가입, 로그인, 홈 등 users 앱의 모든 주소 연결
    path('', include('users.urls')),
]