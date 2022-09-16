from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth.decorators import user_passes_test

urlpatterns = [
    path("", views.index, name="home"),

    path("add-category", views.add_category, name="add-category"),
    path("add-item", views.add_item, name="add-item"),
    path("item/edit/<int:pk>", user_passes_test(lambda user: user.groups.filter(name="moderators").exists(),
                                                login_url=reverse_lazy("denied"))(views.ItemUpdateView.as_view()),
         name="item-edit"),
    path("item/delete/<int:pk>", user_passes_test(lambda user: user.groups.filter(name="moderators").exists(),
                                                  login_url=reverse_lazy("denied"))(views.ItemDeleteView.as_view()),
         name="item-delete"),
    path("category/<slug:category_slug>/order=<str:ordering>", views.category, name="category"),
    path("category/modify", views.category_modify, name="category-modify"),
    path("item/<int:item_id>", views.item_full, name="item"),
    path("search", views.search, name="search"),
    path("checkout", views.checkout, name="checkout"),
    path("checkout/address/old", views.checkout_old_address, name="checkout-address-old"),
    path("checkout/address/new", views.checkout_new_address, name="checkout-address-new"),
    path("orders/manage/sort=<str:sorting>", views.orders_manage, name="orders-manage"),
    path("orders/change/<int:order_id>", views.orders_change, name="orders-change"),
    path("orders/delete/<int:order_id>", views.orders_delete, name="orders-delete"),
    path("orders/order/<int:order_id>/delete_item/<int:item_id>", views.orders_item_delete, name="orders-item-delete"),
    path("orders/add/<int:item_id>", views.orders_item_add, name="orders-item-add"),
    path("orders/edit/address/<int:pk>", views.AddressUpdateView.as_view(), name="orders-edit-address"),
    path("orders/my", views.orders_my, name="orders-my"),
    path("orders/confirm", views.orders_confirm, name="orders-confirm"),
    path("denied", views.denied, name="denied")
]
