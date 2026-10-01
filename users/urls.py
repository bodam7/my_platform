from django.urls import path
from django.contrib.auth import views as auth_views
from users.views import signup_view, home_view, custom_logout_view

urlpatterns = [
    # 메인 홈 페이지 주소
    path('', home_view, name='home'),
    
    # 회원가입 주소
    path('signup/', signup_view, name='signup'),
    
    # 로그인 주소
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    
    # 로그아웃 주소
    path('logout/', custom_logout_view, name='logout'),
]