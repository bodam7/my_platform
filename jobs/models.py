from django.db import models


class Category(models.Model):
    """
    업종 카테고리 모델 (건설/현장, 제조/생산, 식당/서빙 등)
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="업종명",
        help_text="예: 건설/현장, 제조/생산, 식당/서빙"
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        allow_unicode=True,
        verbose_name="슬러그",
        help_text="URL 주소에 사용될 식별자"
    )
    # --- 아래 두 항목(image, order)을 추가해 주세요! ---
    image = models.ImageField(
        upload_to='categories/', 
        blank=True, 
        null=True, 
        verbose_name="카테고리 이미지"
    )
    order = models.IntegerField(
        default=0, 
        verbose_name="정렬 순서",
        help_text="3x3 화면에 표시될 순서 (작은 숫자가 먼저 나옴)"
    )

    class Meta:
        verbose_name = "카테고리"
        verbose_name_plural = "카테고리 목록"
        ordering = ['order', 'id']  # 정렬 순서 지정

    def __str__(self):
        return self.name


class JobPosting(models.Model):
    """
    구인 공고 모델
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="job_postings",
        verbose_name="업종 카테고리"
    )
    title = models.CharField(max_length=200, verbose_name="공고 제목")
    company_name = models.CharField(max_length=100, verbose_name="업체명")
    location = models.CharField(max_length=200, verbose_name="근무지 위치")
    pay = models.CharField(
        max_length=100, 
        verbose_name="급여 조건", 
        help_text="예: 일급 15만원, 월급 300만원"
    )
    description = models.TextField(verbose_name="상세 내용")

    image = models.ImageField(
        upload_to="job_postings/", 
        null=True, 
        blank=True, 
        verbose_name="공고 대표 이미지"
    )

    is_urgent = models.BooleanField(
        default=False, 
        verbose_name="급구 여부",
        help_text="체크 시 메인/상세 화면에 [급구] 뱃지가 표시됩니다."
    )
    is_closed = models.BooleanField(
        default=False, 
        verbose_name="마감 여부",
        help_text="체크 시 메인/상세 화면에 [마감] 뱃지가 표시됩니다."
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")

    class Meta:
        verbose_name = "구인 공고"
        verbose_name_plural = "구인 공고 목록"
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.company_name}] {self.title}"