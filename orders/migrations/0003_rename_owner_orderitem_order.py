# Generated by Django 5.1.1 on 2024-10-01 04:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_orderitem_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='owner',
            new_name='order',
        ),
    ]
