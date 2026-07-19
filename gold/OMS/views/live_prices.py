from django.http import JsonResponse
from OMS.models.product import Product
from decimal import Decimal  # Import Decimal


def live_prices(request):
    data = []

    for product in Product.objects.all():
        latest = product.base_prices.order_by("-created_at").first()

        product_data = {
            "id": product.id,
            "title": product.title,
            "price": None,
            "buy": None,
            "sell": None,
        }

        if latest:
            # Get price directly from latest if it exists and is not None
            price_value = getattr(latest, 'price', None)
            if price_value is not None:
                product_data["price"] = str(price_value)

            # Get buy price from zaryar_buy_price if it exists and is not None
            buy_value = getattr(latest, 'zaryar_buy_price', None)
            if buy_value is not None:
                product_data["buy"] = str(buy_value)

            # Get sell price from zaryar_sell_price if it exists and is not None
            sell_value = getattr(latest, 'zaryar_sell_price', None)
            if sell_value is not None:
                product_data["sell"] = str(sell_value)

        data.append(product_data)

    return JsonResponse({"products": data})
