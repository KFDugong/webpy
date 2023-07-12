from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Cart, CartItem


# Create your views here.
@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, "carts/cart_detail.html", {"cart": cart})


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += int(request.POST['quantity'])  
    cart_item.save()
    print(f"CartItem: {cart_item}, Quantity: {cart_item.quantity}")
    return redirect("carts:view_cart")

@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()
    if cart_item:
        cart_item.delete()
    return redirect("carts:view_cart")

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.cartitem_set.all().delete()
    return redirect("home")
