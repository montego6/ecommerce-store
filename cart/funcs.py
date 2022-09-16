from webshop.models import Item


def get_cart(request):
    cart = request.session.get('cart', {})
    items_list = []
    total = 0
    db_items = Item.objects.filter(id__in=cart)
    quantities = [cart[str(db_item.id)] for db_item in db_items]
    for db_item, item_quantity in zip(db_items, quantities):
        item = {}
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
