from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from OMS.models.base_price import BasePrice
from OMS.models.category_product_mazaneh import CategoryProductMazaneh
from OMS.models.order import Order
from OMS.models.product import Product


class BasePriceInline(admin.TabularInline):
    model = BasePrice
    extra = 0
    fields = ("price", "zaryar_buy_price", "zaryar_sell_price", "created_at")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)


class CategoryProductMazanehInline(admin.TabularInline):
    model = CategoryProductMazaneh
    extra = 0
    fields = ("category", "buy_mazaneh", "sell_mazaneh")
    autocomplete_fields = ("category",)


class CategoryProductMazanehOnCategoryInline(admin.TabularInline):
    model = CategoryProductMazaneh
    fk_name = "category"
    extra = 0
    fields = ("product", "buy_mazaneh", "sell_mazaneh")
    autocomplete_fields = ("product",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "zaryar_id",
        "zaryar_title",
        "can_buy_online",
        "can_sell_online",
        "latest_base_price",
    )
    list_filter = ("can_buy_online", "can_sell_online")
    search_fields = ("title", "zaryar_title", "zaryar_id")
    ordering = ("title",)
    inlines = (BasePriceInline, CategoryProductMazanehInline)

    @admin.display(description="آخرین قیمت پایه")
    def latest_base_price(self, obj):
        return obj.base_price


@admin.register(BasePrice)
class BasePriceAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "price",
        "zaryar_buy_price",
        "zaryar_sell_price",
        "created_at",
    )
    list_filter = (
        "product",
        ("created_at", DateFieldListFilter),
    )
    date_hierarchy = "created_at"
    autocomplete_fields = ("product",)
    readonly_fields = ("created_at",)
    list_select_related = ("product",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "product",
        "trade_type",
        "status",
        "quantity",
        "final_price",
        "total_price",
        "created_at",
    )
    list_filter = (
        "status",
        "trade_type",
        "product",
        ("created_at", DateFieldListFilter),
    )
    search_fields = ("user__phone_number", "user__username", "product__title")
    autocomplete_fields = ("user", "product")
    readonly_fields = (
        "created_at",
        "updated_at",
        "created_jalali",
        "updated_jalali",
    )
    list_select_related = ("user", "product")
    date_hierarchy = "created_at"
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "product",
                    "trade_type",
                    "status",
                    "quantity",
                    "amount",
                    "final_price",
                    "total_price",
                ),
            },
        ),
        (
            "زمان",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "created_jalali",
                    "updated_jalali",
                ),
            },
        ),
    )

    @admin.display(description="تاریخ ثبت (جلالی)")
    def created_jalali(self, obj):
        return obj.get_created_jalali

    @admin.display(description="تاریخ بروزرسانی (جلالی)")
    def updated_jalali(self, obj):
        return obj.get_updated_jalali


@admin.register(CategoryProductMazaneh)
class CategoryProductMazanehAdmin(admin.ModelAdmin):
    list_display = ("category", "product", "buy_mazaneh", "sell_mazaneh")
    list_filter = ("category", "product")
    autocomplete_fields = ("category", "product")
    search_fields = ("category__title", "product__title")
    list_select_related = ("category", "product")
