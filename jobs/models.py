from django.db import models

class Category(models.Model):
    """업종 카테고리 모델 (경비/보안, 미화/청소, 긴급구인 등)"""
    name = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="업종명",
        help_text="예: 경비/보안, 미화/청소, 긴급구인"
    )
    slug = models.SlugField(
        max_length=50, 
        unique=True, 
        allow_unicode=True, 
        verbose_name="슬러그",
        help_text="URL 주소에 사용될 식별자"
    )
    image = models.ImageField(
        upload_to='categories/', 
        blank=True, 
        null=True, 
        verbose_name="카테고리 이미지"
    )
    order = models.IntegerField(
        default=0, 
        verbose_name="정렬 순서",
        help_text="메인 화면 카테고리 표시 순서 (작은 숫자가 먼저 나옴)"
    )

    class Meta:
        verbose_name = "카테고리"
        verbose_name_plural = "카테고리 목록"
        ordering = ['order', 'id']

    def __str__(self):
        return self.name


class JobPosting(models.Model):
    """구인 공고 모델"""
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="job_postings", 
        verbose_name="업종 카테고리"
    )
    title = models.CharField(
        max_length=200, 
        verbose_name="검색용 제목",
        help_text="예: 강남구 주상복합 아파트 보안요원 모집"
    )
    image = models.ImageField(
        upload_to="job_postings/", 
        null=True, 
        blank=True, 
        verbose_name="공고 대표 이미지"
    )
    youtube_url = models.URLField(
        blank=True, 
        null=True, 
        verbose_name="유튜브 동영상 URL",
        help_text="긴급구인 등 동영상 첨부 시 입력 (예: https://www.youtube.com/watch?v=...)"
    )
    
    # 1~8번 정렬 순서 지정 (지정 시 최신순보다 우선 정렬)
    priority_order = models.IntegerField(
        default=0, 
        verbose_name="고정 순서 (1~8)",
        help_text="1~8 입력 시 해당 위치에 우선 배치됩니다. (0은 기본 최신순 정렬)"
    )
    
    # 기획안 '10초 빠른 업로드'를 위해 선택 입력으로 보완
    company_name = models.CharField(max_length=100, blank=True, default="", verbose_name="업체명")
    location = models.CharField(max_length=200, blank=True, default="", verbose_name="근무지 위치")
    pay = models.CharField(max_length=100, blank=True, default="", verbose_name="급여 조건", help_text="예: 일급 15만원, 월급 300만원")
    description = models.TextField(blank=True, default="", verbose_name="상세 내용")
    
    # 상태 및 확장 필드
    is_urgent = models.BooleanField(default=False, verbose_name="급구 여부", help_text="체크 시 [급구] 뱃지가 표시됩니다.")
    is_vip = models.BooleanField(default=False, verbose_name="VIP/유료 공고 여부", help_text="추후 결제 시스템 확장용 필드")
    is_closed = models.BooleanField(default=False, verbose_name="마감 여부", help_text="체크 시 [마감] 뱃지가 표시됩니다.")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")

    class Meta:
        verbose_name = "구인 공고"
        verbose_name_plural = "구인 공고 목록"
        ordering = ['-priority_order', '-created_at']

    def __str__(self):
        return f"[{self.company_name or '공고'}] {self.title}"


class Application(models.Model):
    """즉시 지원하기 모델 (이름 + 전화번호 저장)"""
    job_posting = models.ForeignKey(
        JobPosting, 
        on_delete=models.CASCADE, 
        related_name="applications", 
        verbose_name="지원 공고"
    )
    name = models.CharField(max_length=50, verbose_name="지원자 이름")
    phone_number = models.CharField(max_length=20, verbose_name="전화번호")
    applied_at = models.DateTimeField(auto_now_add=True, verbose_name="지원 일시")

    class Meta:
        verbose_name = "지원 내역"
        verbose_name_plural = "지원 내역 목록"
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.name} ({self.phone_number}) - {self.job_posting.title}"