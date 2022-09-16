from webshop.models import Item


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

    return items_list, total


def get_promo(request):
    promo = request.session.get("promocode", None)
    return promo


def clear_cart(request):
    request.session["cart"] = {}
    request.session["promocode"] = None
