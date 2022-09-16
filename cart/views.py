from django.shortcuts import render, redirect
from django.contrib import messages
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


def get_cart(request):
    cart = request.session.get('cart', {})
    items_list = []
    total = 0
    for item_id, item_quantity in cart.items():
        item = {}
        db_item = Item.objects.get(pk=item_id)
        item["id"] = db_item.id
        item["name"] = db_item.name
        item["quantity"] = item_quantity
        item["price"] = db_item.price
        item["value"] = item["price"] * item["quantity"]
        item["inventory"] = db_item.quantity
        total += item["value"]
        items_list.append(item)
    promo = request.session.get("promocode", False)
    return items_list, total, promo


def view_cart(request):
    items_list, total, promo = get_cart(request)
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