# Generated by Django 5.1.1 on 2025-02-19 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0005_alter_iphonemodel_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="banner",
            name="product",
        ),
        migrations.AddField(
            model_name="banner",
            name="image",
            field=models.ImageField(null=True, upload_to="media/"),
        ),
    ]
