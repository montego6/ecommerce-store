# Generated by Django 4.0.5 on 2022-09-16 15:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0015_promo_alter_order_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='promo',
            name='discount',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
    ]
