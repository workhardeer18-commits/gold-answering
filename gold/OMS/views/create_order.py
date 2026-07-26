from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from OMS.models.base_price import BasePrice
from OMS.models.category_product_mazaneh import CategoryProductMazaneh
from OMS.models.order import Order
from OMS.models.product import Product


def get_user_specific_prices(user, product):
    base_price_obj = BasePrice.objects.filter(
        product=product
    ).order_by("-created_at").first()

    if not base_price_obj:
        return None

    if (
            base_price_obj.zaryar_buy_price is None or
            base_price_obj.zaryar_sell_price is None
    ):
        return None

    mazaneh_entry = CategoryProductMazaneh.objects.filter(
        category=user.category,
        product=product
    ).first()

    buy_offset = mazaneh_entry.buy_mazaneh
    sell_offset = mazaneh_entry.sell_mazaneh

    zaryar_buy = base_price_obj.zaryar_buy_price
    zaryar_sell = base_price_obj.zaryar_sell_price

    price_to_buy_from_us = zaryar_sell + sell_offset
    price_to_sell_to_us = max(zaryar_buy - buy_offset, Decimal("0"))

    return {
        "price_to_buy": price_to_buy_from_us,
        "price_to_sell": price_to_sell_to_us,
        "buy_offset": buy_offset,
        "sell_offset": sell_offset,
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
    if not user_prices:
        messages.error(request, "قیمت این محصول در حال حاضر در دسترس نیست.")
        return redirect("user_dashboard")

    if trade_type == "buy":
        raw_amount = request.POST.get("amount", "0")

        try:
            amount = Decimal(raw_amount)
        except (InvalidOperation, ValueError, TypeError):
            messages.error(request, "مبلغ نامعتبر است.")
            return redirect("user_dashboard")

        final_price = user_prices["price_to_buy"]

        if final_price <= 0:
            messages.error(request, "قیمت در دسترس نیست.")
            return redirect("user_dashboard")

        quantity = amount / final_price

    elif trade_type == "sell":
        raw_quantity = request.POST.get("quantity", "0")

        try:
            quantity = Decimal(raw_quantity)
        except (InvalidOperation, ValueError, TypeError):
            messages.error(request, "مقدار طلا نامعتبر است.")
            return redirect("user_dashboard")

        final_price = user_prices["price_to_sell"]

        if final_price <= 0:
            messages.error(request, "قیمت در دسترس نیست.")
            return redirect("user_dashboard")

        amount = quantity * final_price

    else:
        messages.error(request, "نوع معامله نامعتبر است.")
        return redirect("user_dashboard")

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

    return render(request, "create_order.html", {
        "show_result": True,
        "final_price": final_price,
        "quantity": round(quantity, 6),
        "amount": amount,
        "product": product,
        "trade_type": trade_type,
    })
