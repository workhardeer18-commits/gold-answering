from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from OMS.models.product import Product
from OMS.views.create_order import get_user_specific_prices


@login_required
def product_list(request):
    json = request.GET.get('json', False)
    products = Product.objects.all()

    # برای هر محصول، قیمت اختصاصی کاربر را محاسبه و به شیء محصول اضافه می‌کنیم
    for product in products:
        prices = get_user_specific_prices(request.user, product)
        if prices:
            product.current_buy_price = prices["price_to_buy"]
            product.current_sell_price = prices["price_to_sell"]
        else:
            product.current_buy_price = "ناموجود"
            product.current_sell_price = "ناموجود"

    if json:
        return JsonResponse({"products": products})

    return render(request, "product_list.html", {"products": products})
