from django.conf import settings
from django.db import models
import jdatetime
from OMS.models.product import Product

STATUS_CHOICES = [
        ('pending', 'در انتظار بررسی'),
        ('approved', 'تأیید شده'),
        ('rejected', 'رد شده'),
    ]

TRADE_CHOICES = [
    ('buy', 'خرید'),
    ('sell', 'فروش')
]
class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders',  null=True, blank=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    final_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=0)
    trade_type = models.CharField(max_length=10, choices=TRADE_CHOICES, default='buy', null=True, blank=True)
    quantity = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=0)
    # مبلغ کل ریالی که همان amount شماست، اما داشتن فیلد جداگانه برای شفافیت بهتر است
    total_price =  models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=0)



    def __str__(self):
        return f"{self.created_at}, {self.updated_at}, {self.user}, {self.amount}, {self.status}, {self.product}, {self.final_price}, {self.quantity}, {self.total_price}"

    class Meta:
        ordering = ['-created_at']

    @property
    def get_created_jalali(self):
        return jdatetime.datetime.fromgregorian(datetime=self.created_at).strftime('%Y/%m/%d - %H:%M')

    @property
    def get_updated_jalali(self):
        return jdatetime.datetime.fromgregorian(datetime=self.updated_at).strftime('%Y/%m/%d - %H:%M')




