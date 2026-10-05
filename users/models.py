from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    # 내국인 / 외국인 구분 (local / foreigner)
    USER_TYPE_CHOICES = (
        ('local', '내국인'),
        ('foreigner', '외국인'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='local', verbose_name='사용자 유형')

    # 전화번호 (중복 방지 및 로그인/연락 용도)
    phone_number = models.CharField(max_length=20, unique=True, verbose_name='전화번호')

    # 출생연도 (4자리 숫자)
    birth_year = models.IntegerField(null=True, blank=True, verbose_name='출생연도')

    # 성별
    gender = models.CharField(max_length=10, blank=True, null=True, verbose_name='성별')

    # 외국인 전용 필드
    nationality = models.CharField(max_length=50, blank=True, null=True, verbose_name='국적')
    visa_type = models.CharField(max_length=50, blank=True, null=True, verbose_name='비자 종류')

    # 개인정보 수집 및 이용 동의 (필수)
    agree_privacy_policy = models.BooleanField(default=False, verbose_name='개인정보 수집 및 이용 동의')

    # 포인트 마케팅 시스템을 위한 포인트 필드
    points = models.IntegerField(default=0, verbose_name='보유 포인트')

    # 최근 접속일 (미니 CRM 필터링용)
    last_login_date = models.DateTimeField(auto_now=True, verbose_name='최근 접속일')

    # 기본 auth.User와의 충돌을 방지하기 위한 related_name 설정
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="custom_user_set",
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_set",
        related_query_name="custom_user",
    )

    def __str__(self):
        return f"{self.username} ({self.phone_number})"
    # ==================== 사이트 기본 설정 (로고 관리) ====================
class SiteConfig(models.Model):
    """
    사이트 전체 설정을 관리하는 모델 (로고, 사이트명 등)
    """
    site_name = models.CharField("사이트 이름", max_length=50, default="일자리플랫폼")
    logo = models.ImageField("로고 이미지", upload_to="site_logo/", blank=True, null=True, help_text="상단 헤더에 표시될 로고 이미지 (추천: PNG, 가로형 이미지)")
    updated_at = models.DateTimeField("최종 수정일", auto_now=True)

    class Meta:
        verbose_name = "사이트 기본 설정"
        verbose_name_plural = "사이트 기본 설정"

    def __str__(self):
        return self.site_name