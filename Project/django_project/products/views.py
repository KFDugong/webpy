from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from django.contrib.auth.decorators import permission_required
from .forms import ProductForm
from reviews.forms import CommentForm, RatingForm
from reviews.models import Comment, Rating
from django.db.models import Q, Avg

# Create your views here.


# def product_list(request):
#     products = Product.objects.all().order_by("name")
#     return render(request, "products/product_list.html", {"products": products})


def product_list(request):
    query = request.GET.get("q")
    sort_by = request.GET.get("sort_by")

    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    if sort_by:
        if sort_by == "name":
            products = products.order_by("name")
        elif sort_by == "price":
            products = products.order_by("price")
        elif sort_by == "average_rating":
            products = products.annotate(average_rating=Avg("rating__rating")).order_by(
                "-average_rating"
            )

    return render(request, "products/product_list.html", {"products": products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "products/product_detail.html", {"product": product})


@permission_required("products.add_product")
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("products:product_list")
    else:
        form = ProductForm()
    return render(request, "products/product_create.html", {"form": form})


@permission_required("products.change_product")
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("products:product_detail", pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, "products/product_update.html", {"form": form})


@permission_required("products.delete_product")
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("products:product_list")
    return render(
        request, "products/product_confirm_delete.html", {"product": product}
    )


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comments = Comment.objects.filter(product=product)
    ratings = Rating.objects.filter(product=product)
    rating_form = RatingForm()
    comment_form = CommentForm()

    if request.method == "POST":
        if request.POST.get("action") == "review":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.product = product
                comment.save()
                comment_form = CommentForm()
        elif request.POST.get("action") == "rating":
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.user = request.user
                rating.product = product
                rating.save()
                rating_form = RatingForm()
    context = {
        "product": product,
        "comments": comments,
        "ratings": ratings,
        "comment_form": comment_form,
        "rating_form": rating_form,
    }

    return render(request, "products/product_detail.html", context)
