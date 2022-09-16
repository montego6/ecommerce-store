from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path("", views.view_cart, name="view-cart"),
    path("add/<int:item_id>", views.add_to_cart, name="add-to-cart"),
    path("modify/<int:item_id>", views.cart_modify, name="cart-modify"),
    path("delete/<int:item_id>", views.cart_delete, name="cart-delete")
]