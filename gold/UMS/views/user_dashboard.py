from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from OMS.models.product import Product
from OMS.views.create_order import get_user_specific_prices


@login_required(login_url="/do_login/")
def user_dashboard(request):
    products = Product.objects.all()

    for p in products:
        user_prices = get_user_specific_prices(request.user, p)
        p.display_buy_price = user_prices['price_to_buy']
        p.display_sell_price = user_prices['price_to_sell']

    if request.method == 'GET':
        return render(request, 'user_dashboard.html', {"products": products})
    else:
        return HttpResponse("Method Not Allowed", status=405)
