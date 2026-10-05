from .models import SiteConfig

def site_config(request):
    """
    모든 템플릿에서 site_config 변수를 통해
    사이트 이름 및 관리자 등록 로고에 접근할 수 있도록 제공합니다.
    """
    config = SiteConfig.objects.first()
    return {
        'site_config': config
    }