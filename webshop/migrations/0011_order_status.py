# Generated by Django 4.0.4 on 2022-06-14 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0010_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('process', 'В обработке'), ('delivery', 'Доставляется'), ('finished', 'Завершен')], default='process', max_length=20),
        ),
    ]