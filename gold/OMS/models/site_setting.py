from django.db import models

class SiteSetting(models.Model):
    is_under_maintenance = models.BooleanField(
        "حالت تعطیلات سایت", default=False
    )
    maintenance_message = models.TextField(
        "پیام تعطیلات", default="سایت موقتاً در دست تعمیر است."
    )

    class Meta:
        verbose_name = "تنظیمات سایت"
        verbose_name_plural = "تنظیمات سایت"
