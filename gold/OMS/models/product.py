from django.db import models
from decimal import Decimal


PRODUCTS = [
    {"title": "سکه تاریخ پایین", "endpoint": "zaryar_low_date_coin"},
    {"title": "ربع تاریخ پایین", "endpoint": "zaryar_low_date_quarter"},
    {"title": "نیم تاریخ پایین", "endpoint": "zaryar_low_date_half"},
    {"title": "ربع سکه عادی", "endpoint": "zaryar_regular_quarter"},
    {"title": "ساچمه نقره 995", "endpoint": "zaryar_silver_shot_995"},
    {"title": "شمش نقره 1000 گرمی نادیر ترکیه", "endpoint": "zaryar_nadir_1000"},
    {"title": "ساچمه نقره 999/9", "endpoint": "zaryar_silver_shot_9999"},
    {"title": "ساچمه نقره 990", "endpoint": "zaryar_silver_shot_990"},
    {"title": "شمش نقره 1000 گرمی 999.9 اماراتی", "endpoint": "zaryar_emirates_9999_1000"},
    {"title": "شمش نقره 1000 گرمی 999 اماراتی", "endpoint": "zaryar_emirates_999_1000"},
    {"title": "ربع سکه 1404", "endpoint": "zaryar_quarter_1404"},
    {"title": "آبشده نقد فردا طلانت", "endpoint": "zaryar_talant_cash_tomorrow"},
    {"title": "تمام سکه 1404", "endpoint": "zaryar_full_coin_1404"},
]



# 🔹 دیکشنری سریع برای lookup
PRODUCT_MAP = {p["title"]: p["endpoint"] for p in PRODUCTS}

# 🔹 تولید خودکار dropdown از PRODUCTS
TITLE_ENUM = [(p["title"], p["title"]) for p in PRODUCTS]


class Product(models.Model):
    zaryar_id = models.IntegerField(
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

    title = models.CharField(max_length=255, choices=TITLE_ENUM)
    can_buy_online = models.BooleanField(
        default=True,
        verbose_name="امکان خرید آنلاین توسط کاربر"
    )
    can_sell_online = models.BooleanField(
        default=True,
        verbose_name="امکان فروش آنلاین توسط کاربر"
    )
    endpoint = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        editable=False
    )

    def save(self, *args, **kwargs):
        self.endpoint = PRODUCT_MAP.get(self.title)
        super().save(*args, **kwargs)

    @property
    def base_price(self):
        latest = self.base_prices.order_by("-created_at").first()
        return latest.price if latest else Decimal("5")

    def __str__(self):
        return self.title
