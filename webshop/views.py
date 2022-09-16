from django.shortcuts import render, redirect, Http404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic.edit import UpdateView, DeleteView
from django.forms import modelform_factory, modelformset_factory
from .forms import CategoryForm, ItemForm, StatusForm, RegisteredAddressForm, PromocodeForm, OrderAddItemForm, PromoForm
from .models import Category, Item, Address, Order, OrderItem
from cart.views import get_cart, get_promo
from django.contrib.auth.decorators import user_passes_test
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


# Create your views here.

PROMO = ["SHOP", "KIRILL", "PROMO"]


def categories(request):
    categories_list = Category.objects.all()
    cart_length = len(request.session.get('cart', {}))
    return {
        "categories": categories_list,
        "cart_length": cart_length
    }


def index(request):
    popular = Item.objects.order_by("-orders")[:3]
    last = Item.objects.order_by("quantity")[:3]
    return render(request, "index.html", {"popular": popular, "last": last})


@user_passes_test(lambda user: user.groups.filter(name="moderators").exists(), login_url=reverse_lazy("denied"))
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CategoryForm()
    return render(request, 'form.html', {"form": form, "title": "Добавить категорию"})


def category(request, category_slug, ordering):
    selected_category = Category.objects.get(slug=category_slug)
    if ordering == "popular":
        items = selected_category.items.order_by("-orders")
    elif ordering == "name":
        items = selected_category.items.order_by("name")
    elif ordering == "price-lowest":
        items = selected_category.items.order_by("price")
    elif ordering == "price-highest":
        items = selected_category.items.order_by("-price")
    else:
        raise Http404
    return render(request, "category.html", {'category': selected_category, "items": items})


@user_passes_test(lambda user: user.groups.filter(name="moderators").exists(), login_url=reverse_lazy("denied"))
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('category', category_slug=form.cleaned_data["category"].slug, ordering="popular")
    else:
        form = ItemForm()
    return render(request, 'form.html', {"form": form, "title": "Добавить позицию"})


class ItemUpdateView(UpdateView):
    model = Item
    fields = ['name', 'title', 'image', 'description', 'category', 'quantity', 'price']
    template_name_suffix = '_update'

    def get_success_url(self):
        slug = self.object.category.slug
        return reverse("category", kwargs={"category_slug": slug, "ordering": "popular"})


class ItemDeleteView(DeleteView):
    model = Item

    def get_success_url(self):
        slug = self.object.category.slug
        return reverse("category", kwargs={"category_slug": slug, "ordering": "popular"})


def item_full(request, item_id):
    selected_item = Item.objects.get(pk=item_id)
    return render(request, 'item.html', {"item": selected_item})


def search(request):
    search_query = request.POST["search_input"]
    items_case = Item.objects.filter(name__contains=search_query)
    items_non_case = Item.objects.filter(name__contains=search_query.title())
    items = items_case.union(items_non_case)
    return render(request, "search.html", {"items": items})


def checkout(request):
    if request.method == "POST":
        form = PromocodeForm(request.POST)
        if form.is_valid():
            promocode = form.cleaned_data["promocode"]
            if promocode in PROMO:
                request.session['promocode'] = True
            else:
                request.session['promocode'] = False
                messages.error(request, "Вы ввели недействительный промокод. Попробуйте еще раз или продолжите без промокода")
    else:
        form = PromocodeForm()

    items, total, promo = get_cart(request)
    for item in items:
        if item["quantity"] > item["inventory"]:
            cart = request.session["cart"]
            cart[str(item["id"])] = item["inventory"]
            request.session["cart"] = cart
            messages.error(request, f"Количество товара {item['name']} было скорректировано")
            return redirect("checkout")

    return render(request, "checkout.html", {"items": items, "total": total, "form": form})


def checkout_save_order(request, form_choices, address):
    items, total = get_cart(request)
    promo = get_promo(request)
    order = form_choices.save(commit=False)
    order.address = address
    if promo:
        order.promo = 0.8
        total *= 0.8
    order.total = total
    if request.user.is_authenticated:
        order.user = request.user
    order.save()
    return order


def checkout_old_address(request):
    items, total = get_cart(request)

    if request.method == "POST":
        form_address = RegisteredAddressForm(request.POST, user=request.user)
        if form_address.is_valid():
            address = form_address.cleaned_data["address"]
        form_choices = modelform_factory(Order, fields=["delivery", "payment"])(request.POST)
        order = checkout_save_order(request, form_choices, address)
        order_manage_items(request, order)
        request.session["cart"] = {}
        request.session["promocode"] = False
        send_confirmation_mail(order)
        messages.success(request,
                         f"Заказ #{order.id} успешно создан. Дождитесь звонка оператора для подтверждения заказа")
        return redirect("orders-confirm")

    else:
        form_address = RegisteredAddressForm(user=request.user)
        form_choices = modelform_factory(Order, fields=["delivery", "payment"])

    return render(request, "checkout-address.html", {"items": items, "total": total,
                                                     "form1": form_address,
                                                     "form2": form_choices,
                                                     "address": 'old'})


def checkout_new_address(request):
    items, total = get_cart(request)

    if request.method == "POST":
        form_address = modelform_factory(Address, exclude=["user"])(request.POST)
        if form_address.is_valid():
            address = form_address.save(commit=False)
            if request.user.is_authenticated:
                address.user = request.user
            address.save()
        form_choices = modelform_factory(Order, fields=["delivery", "payment"])(request.POST)
        order = checkout_save_order(request, form_choices, address)
        order_manage_items(request, order)
        request.session["cart"] = {}
        request.session["promocode"] = False
        send_confirmation_mail(order)
        messages.success(request,
                         f"Заказ #{order.id} успешно создан. Дождитесь звонка оператора для подтверждения заказа")
        return redirect("orders-confirm")

    else:
        form_address = modelform_factory(Address, exclude=["user"])
        form_choices = modelform_factory(Order, fields=["delivery", "payment"])

    return render(request, "checkout-address.html", {"items": items, "total": total,
                                                     "form1": form_address,
                                                     "form2": form_choices,
                                                     "address": 'new'})


def order_manage_items(request, order):
    items, total = get_cart(request)
    for item in items:
        db_item = Item.objects.get(id=item["id"])
        order_item, created = OrderItem.objects.get_or_create(item=db_item, quantity=item["quantity"])
        order.items.add(order_item)
        db_item.quantity -= item["quantity"]
        db_item.orders += 1
        db_item.save()


@user_passes_test(lambda user: user.groups.filter(name="moderators").exists(), login_url=reverse_lazy("denied"))
def orders_manage(request, sorting):
    if sorting == "all":
        orders = Order.objects.order_by("-id")
    elif sorting == "process":
        orders = Order.objects.filter(status="process").order_by("-id")
    elif sorting == "confirmed":
        orders = Order.objects.filter(status="confirmed").order_by("-id")
    elif sorting == "delivery":
        orders = Order.objects.filter(status="delivery").order_by("-id")
    elif sorting == "finished":
        orders = Order.objects.filter(status="finished").order_by("-id")
    elif sorting == "last":
        orders = Order.objects.order_by("-id")[:10]
    else:
        raise Http404
    form = StatusForm()
    return render(request, "orders.html", {"all_orders": orders, "form": form})


@user_passes_test(lambda user: user.groups.filter(name="moderators").exists(), login_url=reverse_lazy("denied"))
def orders_change(request, order_id):
    form = StatusForm(request.POST)
    if form.is_valid():
        order = Order.objects.get(id=order_id)
        order.status = form.cleaned_data["status"]
        order.save()
    return redirect("orders-manage", sorting="all")


def orders_delete(request, order_id):
    order = Order.objects.get(id=order_id)
    for item in order.items.all():
        item.item.quantity += item.quantity
        item.item.orders -= 1
        item.item.save()
    order.delete()
    if request.user.groups.filter(name="moderators").exists():
        return redirect("orders-manage", sorting="all")
    else:
        return redirect("orders-my")


@user_passes_test(lambda user: user.groups.filter(name="moderators").exists(), login_url=reverse_lazy("denied"))
def orders_item_delete(request, order_id, item_id):
    order = Order.objects.get(id=order_id)
    item = OrderItem.objects.get(id=item_id)
    item.item.quantity += item.quantity
    item.item.orders -= 1
    item.item.save()
    order.items.remove(item)
    order.total -= order.promo * item.item.price * item.quantity
    order.save()
    return redirect("orders-manage", sorting="all")


@user_passes_test(lambda user: user.groups.filter(name="moderators").exists(), login_url=reverse_lazy("denied"))
def orders_item_add(request, item_id):
    if request.method == "POST":
        form = OrderAddItemForm(request.POST)
        if form.is_valid():
            db_item = Item.objects.get(id=item_id)
            order_item, created = OrderItem.objects.get_or_create(item=db_item, quantity=form.cleaned_data["quantity"])
            order = form.cleaned_data["order"]
            order.items.add(order_item)
            order.total += order.promo * db_item.price
            order.save()
            db_item.quantity -= form.cleaned_data["quantity"]
            db_item.orders += 1
            db_item.save()
            return redirect("orders-manage", sorting="all")
    else:
        form = OrderAddItemForm()
    return render(request, "form.html", {"form": form, "title": "Добавить позицию"})


class AddressUpdateView(UpdateView):
    model = Address
    fields = ['name', 'phone', 'email', 'city', 'address', 'comments']
    template_name_suffix = '_update'

    def get_success_url(self):
        return reverse("orders-manage", kwargs={"sorting": "all"})


def orders_my(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "orders_my.html", {"orders": orders})


def orders_confirm(request):
    return render(request, "message.html")


def denied(request):
    return render(request, "denied.html")


def send_confirmation_mail(order):
    subject = f'Вы сделали заказ #{order.id} в магазине Webshop'
    html_message = render_to_string('webshop/mail_order.html', {'order': order})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to_email = order.address.email

    mail.send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)


def category_modify(request):
    if request.method == "POST":
        form = modelformset_factory(Category, fields=["name", "slug"])(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = modelformset_factory(Category, fields=["name", "slug"])
    return render(request, "form.html", {"form": form})


def admin_panel(request):
    return render(request, "admin.html")


def add_promo(request):
    if request.method == 'POST':
        form = PromoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-panel')
    else:
        form = PromoForm()
    return render(request, 'form.html', {"form": form, "title": "Добавить промокод"})
























