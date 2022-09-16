from cart.funcs import get_cart, get_promo
from .models import Promo, Category, Item, OrderItem
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def categories(request):
    categories_list = Category.objects.all()
    cart_length = len(request.session.get('cart', {}))
    return {
        "categories": categories_list,
        "cart_length": cart_length
    }


def moderator(request):
    return {
        "moderator": request.user.groups.filter(name="moderators").exists()
    }


def check_promo(promocode):
    return Promo.objects.get(name=promocode) if promocode else None


def checkout_save_order(request, form_choices, address):
    items, total = get_cart(request)
    promo = check_promo(get_promo(request))
    order = form_choices.save(commit=False)
    order.address = address
    if promo:
        order.promo = promo.discount_price
        total *= promo.discount_price
    order.total = total
    if request.user.is_authenticated:
        order.user = request.user
    order.save()
    return order


def order_manage_items(request, order):
    items, total = get_cart(request)
    for item in items:
        db_item = Item.objects.get(id=item["id"])
        order_item, created = OrderItem.objects.get_or_create(item=db_item, quantity=item["quantity"])
        order.items.add(order_item)
        db_item.quantity -= item["quantity"]
        db_item.orders += 1
        db_item.save()


def send_confirmation_mail(order):
    subject = f'Вы сделали заказ #{order.id} в магазине Webshop'
    html_message = render_to_string('webshop/mail_order.html', {'order': order})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to_email = order.address.email

    mail.send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)


