# Generated by Django 5.1.1 on 2025-02-16 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "products",
            "0004_coloroption_iphoneseries_storageoption_iphonemodel_and_more",
        ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="iphonemodel",
            options={},
        ),
        migrations.AlterModelOptions(
            name="iphonevariant",
            options={},
        ),
        migrations.AlterUniqueTogether(
            name="iphonemodel",
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name="iphonemodel",
            name="color_options",
        ),
        migrations.RemoveField(
            model_name="iphonemodel",
            name="storage_options",
        ),
    ]
