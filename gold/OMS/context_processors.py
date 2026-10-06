from .models.site_setting import SiteSetting

def site_settings(request):
    return {
        'site_settings': SiteSetting.objects.first()
    }
