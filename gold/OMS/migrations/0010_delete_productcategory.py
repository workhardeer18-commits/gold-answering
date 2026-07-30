from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("OMS", "0009_remove_product_endpoint_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="ProductCategory",
        ),
    ]
