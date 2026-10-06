from django.db import models


class SiteSetting(models.Model):
    is_trading_active = models.BooleanField(default=True, verbose_name="فعال بودن معاملات")
    closed_message = models.CharField(
        max_length=255,
        default="بازار در حال حاضر بسته است. لطفاً بعداً مراجعه کنید.",
        verbose_name="پیام بسته بودن بازار",
    )

    class Meta:
        verbose_name = "تنظیمات سایت"
        verbose_name_plural = "تنظیمات سایت"

    def save(self, *args, **kwargs):
        # فقط اجازه یک رکورد
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
