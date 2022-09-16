# Generated by Django 4.0.5 on 2022-06-13 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0005_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webshop.item')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery', models.CharField(choices=[('selfpick', 'Самовывоз: бесплатно'), ('courier', 'Доставка курьером: 300 руб.'), ('post', 'Доставка почтой: 300 руб.')], max_length=20)),
                ('payment', models.CharField(choices=[('cash', 'Наличными при получении'), ('online', 'Банковской картой онлайн'), ('card', 'Банковской картой при получении')], max_length=20)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='webshop.address')),
                ('items', models.ManyToManyField(to='webshop.orderitem')),
            ],
        ),
    ]