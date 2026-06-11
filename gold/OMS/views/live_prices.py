from django.http import JsonResponse
from OMS.models.product import Product


def live_prices(request):
    products = Product.objects.all()

    data = []
    for product in products:
        data.append({
            "id": product.id,
            "price": str(product.base_price)
        })

    return JsonResponse({"products": data})
