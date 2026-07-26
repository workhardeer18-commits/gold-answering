# در فایل views مربوطه
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from OMS.models.product import Product
from OMS.views.create_order import get_user_specific_prices

@login_required(login_url="/do_login/")
def user_dashboard(request):
    products = Product.objects.all()
    for p in products:
        user_prices = get_user_specific_prices(request.user, p)
        # استفاده از متد .get امن، بدون براکت مستقیم
        p.display_buy_price = user_prices.get('price_to_buy', 0) if user_prices else 0
        p.display_sell_price = user_prices.get('price_to_sell', 0) if user_prices else 0
        p.current_base_price = user_prices.get('base_price', 0) if user_prices else 0

    return render(request, 'user_dashboard.html', {"products": products})
