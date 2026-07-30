import json
import logging

from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from OMS.models.base_price import BasePrice
from OMS.models.product import Product

logger = logging.getLogger(__name__)

REQUIRED_FIELDS = {"Title", "BuyPrice", "SellPrice", "BasePrice", "MarketIsOpen", "Id"}


def _parse_webhook_payload(request):
    """
    Parse JSON array from raw body. Also accepts a single object (wrapped as one-item list)
    and common form field names if the body is empty.
    Returns (payload_list, error_message).
    """
    raw = request.body
    if not raw and request.POST:
        for key in ("payload", "data", "json", "body"):
            if key in request.POST:
                raw = request.POST[key].encode("utf-8")
                break

    if not raw:
        return None, "Empty request body; send a JSON array with Content-Type: application/json"

    text = raw.decode("utf-8-sig").strip()
    if not text:
        return None, "Empty request body; send a JSON array with Content-Type: application/json"

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return None, f"Invalid JSON: {exc.msg} (line {exc.lineno}, column {exc.colno})"

    if isinstance(data, dict):
        data = [data]

    if not isinstance(data, list):
        return None, "Payload must be a JSON array of product objects"

    return data, None


def _resolve_or_create_product(zaryar_id, zaryar_title):
    """Return (product, product_was_created)."""
    product = None
    if zaryar_id is not None:
        product = Product.objects.filter(zaryar_id=zaryar_id).first()

    if not product and zaryar_title:
        product = Product.objects.filter(title__iexact=zaryar_title).first()
        if product and zaryar_id is not None and product.zaryar_id != zaryar_id:
            product.zaryar_id = zaryar_id
            product.save(update_fields=["zaryar_id"])

    if product:
        if zaryar_title and product.zaryar_title != zaryar_title:
            product.zaryar_title = zaryar_title
            product.save(update_fields=["zaryar_title"])
        return product, False

    if zaryar_id is None:
        return None, False

    title = (zaryar_title or "").strip() or f"محصول {zaryar_id}"
    zaryar_title_value = (zaryar_title or "").strip() or title

    try:
        product, created = Product.objects.get_or_create(
            zaryar_id=zaryar_id,
            defaults={
                "title": title,
                "zaryar_title": zaryar_title_value,
            },
        )
        return product, created
    except IntegrityError:
        product = Product.objects.filter(zaryar_id=zaryar_id).first()
        if product:
            return product, False
        raise


@csrf_exempt
@require_POST
def zaryar_prices_webhook(request):
    body = request.body.decode("utf-8", errors="replace")
    logger.info(msg=f"Zaryar Request Received, {request.GET}, {request.POST}, {body}")

    payload, parse_error = _parse_webhook_payload(request)
    if parse_error:
        logger.warning("Zaryar webhook parse error: %s", parse_error)
        return JsonResponse({"status": "error", "message": parse_error}, status=400)

    result = {
        "status": "ok",
        "created": 0,
        "products_created": 0,
        "product_not_found": 0,
        "processed": 0,
        "skipped": 0,
    }

    with transaction.atomic():
        for item in payload:
            if not isinstance(item, dict):
                result["skipped"] += 1
                logger.warning("Zaryar webhook: skipping non-object item: %r", item)
                continue

            missing = REQUIRED_FIELDS - item.keys()
            if missing:
                result["skipped"] += 1
                logger.warning(
                    "Zaryar webhook: skipping item missing fields %s: %r",
                    sorted(missing),
                    item,
                )
                continue

            result["processed"] += 1
            zaryar_id = item.get("Id")
            zaryar_title = item.get("Title")

            try:
                product, product_was_created = _resolve_or_create_product(
                    zaryar_id, zaryar_title
                )
            except IntegrityError:
                logger.exception(
                    "Zaryar webhook: failed to resolve product zaryar_id=%s",
                    zaryar_id,
                )
                result["product_not_found"] += 1
                continue

            if not product:
                logger.warning(
                    "Zaryar webhook: product not found and cannot create (no Id): %r",
                    item,
                )
                result["product_not_found"] += 1
                continue

            if product_was_created:
                result["products_created"] += 1

            try:
                BasePrice.objects.create(
                    product=product,
                    price=item.get("BasePrice"),
                    zaryar_buy_price=item.get("BuyPrice"),
                    zaryar_sell_price=item.get("SellPrice"),
                )
                result["created"] += 1
            except Exception:
                logger.exception(
                    "Zaryar webhook: failed to create BasePrice for product %s",
                    product.pk,
                )
                continue

    logger.info(msg=f"Zaryar Result: {result}")
    return JsonResponse(result)
