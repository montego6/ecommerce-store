from django.shortcuts import render, redirect
from django.contrib import messages

from cart.funcs import get_cart
from webshop.models import Item

# Create your views here.


def add_to_cart(request, item_id):
    cart = request.session.get('cart', {})
    db_item = Item.objects.get(pk=item_id)
    if str(item_id) in cart:
        if cart[str(item_id)] < db_item.quantity:
            cart[str(item_id)] += 1
        else:
            messages.error(request, "На складе недостаточное количество товара, в вашей корзине находится максимум")
    else:
        cart[str(item_id)] = 1
    request.session['cart'] = cart
    return redirect('cart:view-cart')


def view_cart(request):
    items_list, total = get_cart(request)
    return render(request, "cart.html", {"items": items_list, "total": total})


def cart_modify(request, item_id):
    new_quantity = request.POST.get('desired_quantity')
    cart = request.session.get('cart', {})
    cart[str(item_id)] = int(new_quantity)
    request.session['cart'] = cart
    return redirect('cart:view-cart')


def cart_delete(request, item_id):
    cart = request.session.get('cart', {})
    del cart[str(item_id)]
    request.session['cart'] = cart
    return redirect('cart:view-cart')