# Generated by Django 4.0.5 on 2022-06-13 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0008_alter_order_delivery_alter_order_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
