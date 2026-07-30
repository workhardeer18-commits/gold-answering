from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.db.models import Count

from OMS.admin import CategoryProductMazanehOnCategoryInline
from OMS.models.order import Order
from UMS.models.user import User
from UMS.models.user_category import UserCategory


class OrderInline(admin.TabularInline):
    model = Order
    fk_name = "user"
    extra = 0
    show_change_link = True
    fields = (
        "product",
        "trade_type",
        "status",
        "quantity",
        "total_price",
        "created_at",
    )
    readonly_fields = ("created_at",)
    autocomplete_fields = ("product",)

    def get_queryset(self, request):
        qs = (
            super()
            .get_queryset(request)
            .select_related("product")
            .order_by("-created_at")
        )
        pks = list(qs.values_list("pk", flat=True)[:50])
        return qs.filter(pk__in=pks)


@admin.register(UserCategory)
class UserCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user_count", "mazaneh_rule_count")
    search_fields = ("title",)
    inlines = (CategoryProductMazanehOnCategoryInline,)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            _user_count=Count("users", distinct=True),
            _mazaneh_rule_count=Count("product_mazaneh", distinct=True),
        )

    @admin.display(description="تعداد کاربران", ordering="_user_count")
    def user_count(self, obj):
        return obj._user_count

    @admin.display(description="تعداد مظنه", ordering="_mazaneh_rule_count")
    def mazaneh_rule_count(self, obj):
        return obj._mazaneh_rule_count


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = (
        "phone_number",
        "username",
        "name",
        "last_name",
        "category",
        "is_admin",
        "is_active",
        "is_staff",
        "date_joined",
    )
    list_filter = (
        "category",
        "is_admin",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    search_fields = (
        "phone_number",
        "username",
        "name",
        "last_name",
        "email",
    )
    autocomplete_fields = ("category",)
    inlines = (OrderInline,)

    fieldsets = DjangoUserAdmin.fieldsets + (
        (
            "اطلاعات تکمیلی",
            {
                "fields": (
                    "phone_number",
                    "name",
                    "category",
                    "is_admin",
                ),
            },
        ),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        (
            "اطلاعات تکمیلی",
            {
                "fields": (
                    "phone_number",
                    "name",
                    "category",
                    "is_admin",
                ),
            },
        ),
    )
