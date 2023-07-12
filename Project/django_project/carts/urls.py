from django.urls import path
from .views import add_to_cart, view_cart, remove_from_cart, checkout

app_name = "carts"

urlpatterns = [
    path("add/<int:pk>/", add_to_cart, name="add_to_cart"),
    path("remove/<int:product_id>/", remove_from_cart, name="remove_from_cart"),
    path("view/", view_cart, name="view_cart"),
    path("checkout/", checkout, name="checkout"),
]
