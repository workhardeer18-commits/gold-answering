from django.db import models


class CategoryProductMazaneh(models.Model):
    category = models.ForeignKey("UMS.UserCategory",related_name="product_mazaneh",on_delete=models.CASCADE)
    product = models.ForeignKey("OMS.Product",related_name="category_mazaneh",on_delete=models.CASCADE)
    buy_mazaneh = models.DecimalField(max_digits=20, decimal_places=0, verbose_name="مظنه خرید", default=0)
    sell_mazaneh = models.DecimalField(max_digits=20, decimal_places=0, verbose_name= "مظنه فروش", default=0)

    class Meta:
        unique_together = (
            "category",
            "product"
        )

    def __str__(self):
        return f"{self.category} - {self.product}, {self.buy_mazaneh}, {self.sell_mazaneh}"


