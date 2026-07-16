from django.db import models


class BasePrice(models.Model):

    product = models.ForeignKey(
        "OMS.Product",
        related_name="base_prices",
        on_delete=models.CASCADE
    )

    price = models.DecimalField(
        max_digits=20,
        decimal_places=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    zaryar_buy_price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="قیمت خرید زریار"
    )

    zaryar_sell_price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="قیمت فروش زریار"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.product} - {self.price}"

