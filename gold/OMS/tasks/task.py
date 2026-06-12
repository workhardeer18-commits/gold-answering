from decimal import Decimal
from datetime import timedelta
from celery import shared_task
from django.utils import timezone
import requests
from OMS.models.base_price import BasePrice
from OMS.models.product import Product



SAVE_INTERVAL_MINUTES = 5
MIN_PERCENT_CHANGE = Decimal("0.001")


@shared_task(max_retries=3)
def test_task():

    urls = [
        "https://call3.tgju.org/ajax.json?rev=jwEkfaXjctiViQ70RAghjp0zVeWDEipltHqrQA57d5G51HHwFGq5NgBSrYgA",
        "https://call3.tgju.org/ajax.json?rev=GIyEx5EcZrwquHYGCAXD4NLPfWGuX3IxB2SFwF7PKtp8YT52Xa1QawJAeTi1",
        "https://call3.tgju.org/ajax.json?rev=Xyd3cPyXkbx00ELZSXgC40CP0oF4y7xxr3rgPg0mz4Gzv5iixpwyLZctFDXG",
        "https://call3.tgju.org/ajax.json?rev=kPUSNvousrDK84GeuVmUuAo7usTKABf64yniQdLwjGmRb5yzilm2ZdDuraz9",
    ]

    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0",
        "referer": "https://www.tgju.org/",
    }

    data = None



    for url in urls:
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            print(f"✅ TGJU connected")
            break
        except Exception as e:
            print(f"Failed URL -> {e}")

    if not data:
        print("All TGJU endpoints failed")
        return

    current_data = data.get("current", {})
    prices = {}

    for endpoint, item in current_data.items():
        if isinstance(item, dict):
            price_str = item.get("p")
            if price_str:
                try:
                    clean_price = price_str.replace(",", "")
                    prices[endpoint] = Decimal(clean_price)
                except Exception:
                    continue


    now = timezone.now()
    updated_count = 0
    skipped_count = 0

    products = Product.objects.all()

    for product in products:
        new_price = prices.get(product.endpoint)

        if not new_price:
            continue

        last_record = product.base_prices.order_by("-created_at").first()


        if not last_record:
            BasePrice.objects.create(product=product, price=new_price)
            updated_count += 1
            continue

        price_changed = last_record.price != new_price
        time_passed = (now - last_record.created_at) > timedelta(minutes=SAVE_INTERVAL_MINUTES)


        if last_record.price > 0:
            percent_change = abs(new_price - last_record.price) / last_record.price
        else:
            percent_change = Decimal("1")

        if price_changed and time_passed and percent_change > MIN_PERCENT_CHANGE:
            BasePrice.objects.create(product=product, price=new_price)
            updated_count += 1
        else:
            skipped_count += 1

    print(
        f"📊 Updated: {updated_count} | "
        f"Skipped: {skipped_count} | "
        f"Total Products: {products.count()}"
    )
