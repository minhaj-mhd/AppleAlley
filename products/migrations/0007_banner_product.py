# Generated by Django 5.1.1 on 2025-02-26 10:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0006_remove_banner_product_banner_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="banner",
            name="product",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="products.iphonevariant",
            ),
        ),
    ]
