from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="uploads", null=True, blank=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField()
    orders = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Address(models.Model):
    name = models.CharField(max_length=50, verbose_name="Ваше имя")
    phone = models.CharField(max_length=50, verbose_name="Ваш телефон")
    email = models.EmailField(verbose_name="Ваш e-mail")
    city = models.CharField(max_length=50, verbose_name="Город", null=True, blank=True)
    address = models.CharField(max_length=200, verbose_name="Полный адрес", null=True, blank=True)
    comments = models.CharField(max_length=200, verbose_name="Комментарий", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="address")

    def __str__(self):
        return f"{self.phone} - {self.city} - {self.address}"


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.item.name} x{self.quantity}"


DELIVERY_CHOICES = [
    ("selfpick", "самовывоз, бесплатно"),
    ("courier", "доставка курьером, 300 руб."),
    ("post", "доставка почтой, 300 руб.")
]

PAYMENT_CHOICES = [
    ("cash", "наличными при получении"),
    ("online", "банковской картой онлайн"),
    ("card", "банковской картой при получении")
]

STATUS_CHOICES = [
    ("process", "в обработке"),
    ("confirmed", "подтвержден"),
    ("delivery", "доставляется"),
    ("finished", "завершен")
]


class Order(models.Model):
    items = models.ManyToManyField(OrderItem)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    delivery = models.CharField(max_length=20, choices=DELIVERY_CHOICES, null=True, blank=True, verbose_name="Доставка")
    payment = models.CharField(max_length=20, choices=PAYMENT_CHOICES, null=True, blank=True, verbose_name="Оплата")
    total = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="process", verbose_name="Статус заказа")
    promo = models.FloatField(default=1)

    def __str__(self):
        return f"{self.id}"