from django.db import models
from decimal import Decimal


PRODUCTS = [
    {"title": "سکه امامی تک فروشی", "endpoint": "retail_sekee"},
    {"title": "سکه بهار آزادی تک فروشی", "endpoint": "retail_sekeb"},
    {"title": "نیم سکه تک فروشی", "endpoint": "retail_nim"},
    {"title": "ربع سکه تک فروشی", "endpoint": "retail_rob"},
    {"title": "سکه گرمی تک فروشی", "endpoint": "retail_gerami"},
    {"title": "ربع سکه", "endpoint": "rob"},
    {"title": "سکه امامی", "endpoint": "sekee"},
    {"title": "سکه بهار آزادی", "endpoint": "sekeb"},
    {"title": "نیم سکه", "endpoint": "nim"},
    {"title": "سکه گرمی", "endpoint": "gerami"},
    {"title": "طلا 18 عیار", "endpoint": "geram18"},
    {"title": "گرم نقره 999", "endpoint": "silver_999"},
    {"title": "مثقال طلا", "endpoint": "mesghal"},
    {"title": "آب شده معاملاتی", "endpoint": "gold_melted_transfer"},
    {"title": "آب شده نقدی", "endpoint": "gold_futures"},
    {"title": "مثقال بدون حباب", "endpoint": "gold_17"},
]


# 🔹 دیکشنری سریع برای lookup
PRODUCT_MAP = {p["title"]: p["endpoint"] for p in PRODUCTS}

# 🔹 تولید خودکار dropdown از PRODUCTS
TITLE_ENUM = [(p["title"], p["title"]) for p in PRODUCTS]


class Product(models.Model):
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
