import json
import logging

from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
logger.info(msg=f"Zaryar Request Received, {request.GET}, {request.POST}")
from OMS.models.base_price import BasePrice
from OMS.models.product import Product

logger = logging.getLogger(__name__)

REQUIRED_FIELDS = {"Title", "BuyPrice", "SellPrice", "BasePrice", "MarketIsOpen", "Id"}


@csrf_exempt
@require_POST
def zaryar_prices_webhook(request):

    try:
        payload = json.loads(request.body)
    except Exception:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    result = {"status": "ok", "created": 0, "product_not_found": 0, "processed": 0}

    with transaction.atomic():
        for item in payload:
            result["processed"] += 1
            zaryar_id = item.get("Id")
            zaryar_title = item.get("Title")

            product = None
            if zaryar_id:
                product = Product.objects.filter(zaryar_id=zaryar_id).first()

            if not product and zaryar_title:
                product = Product.objects.filter(title__iexact=zaryar_title).first()
                if product:
                    product.zaryar_id = zaryar_id
                    product.save(update_fields=['zaryar_id'])

            if not product:
                result["product_not_found"] += 1
                continue

            try:
                BasePrice.objects.create(
                    product=product,
                    price=item.get('BasePrice'),
                    zaryar_buy_price=item.get('BuyPrice'),
                    zaryar_sell_price=item.get('SellPrice')
                )
                result["created"] += 1
            except Exception:
                continue

    logger.info(msg=f'Zaryar Result: {result}')
    return JsonResponse(result)
