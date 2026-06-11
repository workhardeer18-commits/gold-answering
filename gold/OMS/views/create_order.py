from OMS.models.category_product_mazaneh import CategoryProductMazaneh
from decimal import Decimal
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from OMS.models.order import Order
from OMS.models.product import Product

def get_user_specific_prices(user, product):
    base = product.base_price

    # ۲. پیدا کردن تنظیمات مظنه برای این کاربر و این محصول
    try:
        mazaneh_entry = CategoryProductMazaneh.objects.filter(
            category=user.category,
            product=product
        ).first()
    except:
        mazaneh_entry = None

    # ۳. تعیین مقادیر اختلاف (Offset) از فیلدهای جدید مدل شما
    buy_offset = mazaneh_entry.buy_mazaneh if (mazaneh_entry and mazaneh_entry.buy_mazaneh) else Decimal("0")
    sell_offset = mazaneh_entry.sell_mazaneh if (mazaneh_entry and mazaneh_entry.sell_mazaneh) else Decimal("0")

    price_to_buy_from_us = base + sell_offset  # نرخ فروش واحد (مشتری می‌خرد)
    price_to_sell_to_us = base - buy_offset  # نرخ خرید واحد (مشتری می‌فروشد)

    return {
        'price_to_buy': price_to_buy_from_us,
        'price_to_sell': price_to_sell_to_us,
        'buy_offset': buy_offset,
        'sell_offset': sell_offset
    }





@login_required
def create_order(request):

    if request.method != "POST":
        return redirect("user_dashboard")

    product_id = request.POST.get("product")
    trade_type = request.POST.get("trade_type")

    if not product_id or not trade_type:
        messages.error(request, "اطلاعات ناقص است.")
        return redirect("user_dashboard")

    product = get_object_or_404(Product, id=product_id)

    user_prices = get_user_specific_prices(request.user, product)

    # -----------------------
    # ✅ BUY (کاربر مبلغ وارد می‌کند)
    # -----------------------
    if trade_type == "buy":

        raw_amount = request.POST.get("amount", "0")

        try:
            amount = Decimal(raw_amount)
        except:
            messages.error(request, "مبلغ نامعتبر است.")
            return redirect("user_dashboard")

        final_price = user_prices["price_to_buy"]

        if final_price <= 0:
            messages.error(request, "قیمت در دسترس نیست.")
            return redirect("user_dashboard")

        quantity = amount / final_price

    # -----------------------
    # ✅ SELL (کاربر مقدار طلا وارد می‌کند)
    # -----------------------
    elif trade_type == "sell":

        raw_quantity = request.POST.get("quantity", "0")

        try:
            quantity = Decimal(raw_quantity)
        except:
            messages.error(request, "مقدار طلا نامعتبر است.")
            return redirect("user_dashboard")

        final_price = user_prices["price_to_sell"]

        if final_price <= 0:
            messages.error(request, "قیمت در دسترس نیست.")
            return redirect("user_dashboard")

        amount = quantity * final_price

    # -----------------------
    # ✅ اگر trade_type اشتباه بود
    # -----------------------
    else:
        messages.error(request, "نوع معامله نامعتبر است.")
        return redirect("user_dashboard")

    # -----------------------
    # ✅ ثبت نهایی
    # -----------------------
    if "confirm" in request.POST:

        Order.objects.create(
            user=request.user,
            product=product,
            amount=amount,
            total_price=amount,
            quantity=quantity,
            final_price=final_price,
            trade_type=trade_type,
            status="pending"
        )

        messages.success(request, "سفارش با موفقیت ثبت شد.")
        return redirect("user_dashboard")

    # -----------------------
    # ✅ حالت پیش‌نمایش
    # -----------------------
    return render(request, "create_order.html", {
        "show_result": True,
        "final_price": final_price,
        "quantity": round(quantity, 6),
        "amount": amount,
        "product": product,
        "trade_type": trade_type,
    })
