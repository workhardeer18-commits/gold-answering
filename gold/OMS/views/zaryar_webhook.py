import json
import logging
from decimal import Decimal, InvalidOperation

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db import transaction

from OMS.models.base_price import BasePrice
from OMS.models.product import Product

logger = logging.getLogger(__name__)

REQUIRED_FIELDS = {
    "Title",
    "BuyPrice",
    "SellPrice",
    "BasePrice",
    "MarketIsOpen",
    "Id",
}


def _get_client_ip(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


def _to_decimal(value):
    if value is None or isinstance(value, bool):
        raise InvalidOperation
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise InvalidOperation(f"Cannot convert '{value}' to Decimal")


def _get_product_id(item):
    product_id = item.get("Id")
    if product_id is None:
        product_id = item.get("ProductId")
    return product_id


def log_full_request(request):
    try:
        headers = dict(request.headers)
    except Exception as e:
        headers = {"error": str(e)}

    try:
        get_data = request.GET.dict()
    except Exception as e:
        get_data = {"error": str(e)}

    try:
        post_data = request.POST.dict()
    except Exception as e:
        post_data = {"error": str(e)}

    try:
        files_data = {
            key: {
                "name": uploaded_file.name,
                "size": uploaded_file.size,
                "content_type": getattr(uploaded_file, "content_type", None),
            }
            for key, uploaded_file in request.FILES.items()
        }
    except Exception as e:
        files_data = {"error": str(e)}

    try:
        raw_body_text = request.body.decode("utf-8", errors="replace")
    except Exception as e:
        raw_body_text = f"Could not decode body: {e}"

    try:
        parsed_json = json.loads(request.body)
    except Exception as e:
        parsed_json = f"Not valid JSON or empty body: {e}"

    logger.warning("=" * 80)
    logger.warning("ZARYAR WEBHOOK FULL REQUEST DEBUG")
    logger.warning(f"Method: {request.method}")
    logger.warning(f"Path: {request.path}")
    logger.warning(f"Client IP: {_get_client_ip(request)}")
    logger.warning(f"Content-Type: {request.META.get('CONTENT_TYPE')}")
    logger.warning(f"Content-Length: {request.META.get('CONTENT_LENGTH')}")
    logger.warning(f"Headers: {json.dumps(headers, ensure_ascii=False, indent=2)}")
    logger.warning(f"GET params: {json.dumps(get_data, ensure_ascii=False, indent=2)}")
    logger.warning(f"POST params: {json.dumps(post_data, ensure_ascii=False, indent=2)}")
    logger.warning(f"FILES: {json.dumps(files_data, ensure_ascii=False, indent=2)}")
    logger.warning(f"Raw body: {raw_body_text}")
    logger.warning(
        f"Parsed JSON: {json.dumps(parsed_json, ensure_ascii=False, indent=2) if not isinstance(parsed_json, str) else parsed_json}"
    )
    logger.warning("=" * 80)


@csrf_exempt
@require_POST
def zaryar_prices_webhook(request):
    log_full_request(request)

    logger.info(f"Webhook received! Request body: {request.body}")

    try:
        payload = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        logger.error("Received invalid JSON body.")
        return JsonResponse({"status": "error", "message": "Invalid JSON body."}, status=400)

    if not isinstance(payload, list):
        logger.error("JSON body is not a list.")
        return JsonResponse({"status": "error", "message": "JSON body must be a list of products."}, status=400)

    result = {
        "status": "ok",
        "received": len(payload),
        "created": 0,
        "duplicate": 0,
        "market_closed": 0,
        "product_not_found": 0,
        "invalid": 0,
        "processed": 0,
    }

    with transaction.atomic():
        for item in payload:
            result["processed"] += 1

            if not isinstance(item, dict):
                result["invalid"] += 1
                continue

            product_id_from_zaryar = _get_product_id(item)
            if product_id_from_zaryar is None:
                result["invalid"] += 1
                continue

            missing_fields = REQUIRED_FIELDS - item.keys()
            if missing_fields:
                logger.warning(f"Missing required fields {missing_fields} in item: {item}")
                result["invalid"] += 1
                continue

            zaryar_id_str = str(product_id_from_zaryar).strip()
            if not zaryar_id_str:
                result["invalid"] += 1
                continue

            try:
                buy_price = _to_decimal(item["BuyPrice"])
                sell_price = _to_decimal(item["SellPrice"])
                base_price = _to_decimal(item["BasePrice"])
                market_is_open = bool(item["MarketIsOpen"])
            except (TypeError, ValueError, InvalidOperation) as e:
                logger.error(f"Invalid price/market data for item {item}: {e}")
                result["invalid"] += 1
                continue

            try:
                product = Product.objects.get(zaryar_id=zaryar_id_str)
            except Product.DoesNotExist:
                result["product_not_found"] += 1
                continue
            except Product.MultipleObjectsReturned:
                result["invalid"] += 1
                continue

            if not market_is_open:
                result["market_closed"] += 1
                continue

            selected_price = base_price
            if selected_price != selected_price.to_integral_value():
                result["invalid"] += 1
                continue

            latest_price_entry = product.base_prices.order_by("-created_at").first()
            if (
                latest_price_entry is not None
                and latest_price_entry.price == int(selected_price)
                and latest_price_entry.zaryar_buy_price == buy_price
                and latest_price_entry.zaryar_sell_price == sell_price
            ):
                result["duplicate"] += 1
                continue

            try:
                BasePrice.objects.create(
                    product=product,
                    price=int(selected_price),
                    zaryar_buy_price=buy_price,
                    zaryar_sell_price=sell_price,
                )
                result["created"] += 1
            except Exception as e:
                logger.error(f"Error creating BasePrice for Zaryar ID {zaryar_id_str}: {e}")
                result["invalid"] += 1

    logger.info(f"Webhook processing finished. Result: {result}")
    return JsonResponse(result)
