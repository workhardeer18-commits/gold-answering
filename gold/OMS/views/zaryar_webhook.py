import json
from decimal import Decimal, InvalidOperation

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from OMS.models.base_price import BasePrice
from OMS.models.product import Product


REQUIRED_FIELDS = {
    "ProductId",
    "Title",
    "BuyPrice",
    "SellPrice",
    "BasePrice",
    "MarketIsOpen",
}


def _get_client_ip(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR", "")


def _to_decimal(value):
    if value is None or isinstance(value, bool):
        raise InvalidOperation

    return Decimal(str(value))


@csrf_exempt
@require_POST
def zaryar_prices_webhook(request):
    client_ip = _get_client_ip(request)
    allowed_ips = settings.ZARYAR_ALLOWED_IPS

    if allowed_ips and client_ip not in allowed_ips:
        return JsonResponse(
            {
                "status": "error",
                "message": "IP address is not allowed.",
            },
            status=403,
        )

    try:
        payload = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {
                "status": "error",
                "message": "Invalid JSON body.",
            },
            status=400,
        )

    # زریار گفته همه محصولات را در یک درخواست می‌فرستد.
    if not isinstance(payload, list):
        return JsonResponse(
            {
                "status": "error",
                "message": "JSON body must be a list of products.",
            },
            status=400,
        )

    result = {
        "status": "ok",
        "received": len(payload),
        "created": 0,
        "duplicate": 0,
        "market_closed": 0,
        "product_not_found": 0,
        "invalid": 0,
    }

    for item in payload:
        if not isinstance(item, dict):
            result["invalid"] += 1
            continue

        if not REQUIRED_FIELDS.issubset(item):
            result["invalid"] += 1
            continue

        # bool در پایتون زیرمجموعه int است؛ بنابراین جداگانه رد می‌شود.
        if isinstance(item["ProductId"], bool):

            result["invalid"] += 1
            continue

        try:
            zaryar_id = int(item["ProductId"])
            buy_price = _to_decimal(item["BuyPrice"])
            sell_price = _to_decimal(item["SellPrice"])
            base_price = _to_decimal(item["BasePrice"])
        except (TypeError, ValueError, InvalidOperation):
            result["invalid"] += 1
            continue

        if not isinstance(item["MarketIsOpen"], bool):
            result["invalid"] += 1
            continue

        try:
            product = Product.objects.get(zaryar_id=zaryar_id)
        except Product.DoesNotExist:
            result["product_not_found"] += 1
            continue
        except Product.MultipleObjectsReturned:
            result["invalid"] += 1
            continue

        if not item["MarketIsOpen"]:
            result["market_closed"] += 1
            continue

        # تا زمان شفاف‌شدن فرمول زریار، BasePrice را بدون محاسبه ذخیره می‌کنیم.
        selected_price = base_price

        # فیلد price اعشار ندارد؛ پس قیمت پایه باید عدد صحیح باشد.
        if selected_price != selected_price.to_integral_value():
            result["invalid"] += 1
            continue

        latest_price = product.base_prices.first()

        if (
            latest_price is not None
            and latest_price.price == selected_price
            and latest_price.zaryar_buy_price == buy_price
            and latest_price.zaryar_sell_price == sell_price
        ):
            result["duplicate"] += 1
            continue

        BasePrice.objects.create(
            product=product,
            price=selected_price,
            zaryar_buy_price=buy_price,
            zaryar_sell_price=sell_price,
        )
        result["created"] += 1

    return JsonResponse(result)
