from django.shortcuts import render
from django.urls import reverse
from .models.site_setting import SiteSetting


class MaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # اجازه عبور به پنل ادمین، مدیا و فایل‌های استاتیک
        path = request.path_info
        if path.startswith('/admin/') or path.startswith('/static/') or path.startswith('/media/'):
            return self.get_response(request)

        # اگر کاربر سوپریوزر/ادمین باشد سایت برایش باز بماند
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
            return self.get_response(request)

        # بررسی حالت تعمیرات از دیتابیس
        try:
            setting = SiteSetting.objects.first()
            if setting and setting.is_under_maintenance:
                return render(request, 'maintenance.html', {
                    'message': setting.maintenance_message
                }, status=503)
        except Exception:
            # در صورت بروز خطای مقطعی در دیتابیس یا اجرای مایگریشن‌ها، لود سایت متوقف نشود
            pass

        return self.get_response(request)
