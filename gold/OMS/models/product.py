from django.db import models
from decimal import Decimal

class Product(models.Model):
    # اضافه کردن فیلد برای شناسه زریار
    zaryar_id = models.BigIntegerField(
        null=True,
        blank=True,
        unique=True,
        verbose_name="شناسه محصول در زریار"
    )

    zaryar_title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="عنوان محصول در زریار"
    )

    title = models.CharField(max_length=255, )
    can_buy_online = models.BooleanField(
        default=True,
        verbose_name="امکان خرید آنلاین توسط کاربر"
    )
    can_sell_online = models.BooleanField(
        default=True,
        verbose_name="امکان فروش آنلاین توسط کاربر"
    )


    @property
    def base_price(self):
        latest = self.base_prices.order_by("-created_at").first()
        return latest.price if latest else Decimal("5")

    def __str__(self):
        return self.title
