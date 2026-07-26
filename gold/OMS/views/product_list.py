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
            product.price = prices["price"]
        else:
            product.current_buy_price = "ناموجود"
            product.current_sell_price = "ناموجود"
            product.price = "ناموجود"

    if json:
        return JsonResponse({"products": [{
            'id': product.id,
            'title': product.title,
            'buy': product.current_buy_price,
            'sell': product.current_sell_price,
            'price': product.price,
        } for product in products]})

    return render(request, "product_list.html", {"products": products})
