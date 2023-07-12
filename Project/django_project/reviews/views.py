from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Comment, Rating
from products.models import Product
from .forms import CommentForm, RatingForm


# Create your views here.
@login_required
def comment_detail(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    form = CommentForm(instance=comment)
    return render(
        request, "reviews/comment_detail.html", {"form": form, "object": comment}
    )


@login_required
def comment_update(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user == comment.user:
        if request.method == "POST":
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                return redirect("products:product_detail", pk=comment.product.pk)
        else:
            form = CommentForm(instance=comment)
        return render(request, "reviews/comment_update.html", {"form": form})
    else:
        return redirect("products:product_detail", pk=comment.product.pk)


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user == comment.user or request.user.is_staff:
        if request.method == "POST":
            comment.delete()
            return redirect("products:product_detail", pk=comment.product.pk)
    else:
        return redirect("products:product_detail", pk=comment.product.pk)
    return render(request, "reviews/comment_confirm_delete.html", {"comment": comment})


@login_required
def rating_detail(request, pk):
    rating = get_object_or_404(Rating, pk=pk)
    form = RatingForm(instance=rating)
    return render(
        request, "reviews/rating_detail.html", {"form": form, "object": rating}
    )


@login_required
def rating_update(request, pk):
    rating = get_object_or_404(Rating, pk=pk)
    if request.user == rating.user:
        if request.method == "POST":
            form = RatingForm(request.POST, instance=rating)
            if form.is_valid():
                form.save()
                return redirect("products:product_detail", pk=rating.product.pk)
        else:
            form = RatingForm(instance=rating)
        return render(request, "reviews/rating_update.html", {"form": form})
    else:
        return redirect("products:product_detail", pk=rating.product.pk)


@login_required
def rating_delete(request, pk):
    rating = get_object_or_404(Rating, pk=pk)
    if request.user == rating.user:
        if request.method == "POST":
            rating.delete()
            return redirect("products:product_detail", pk=rating.product.pk)
    else:
        return redirect("products:product_detail", pk=rating.product.pk)
    return render(request, "reviews/rating_confirm_delete.html", {"rating": rating})


@login_required
def comment_feedback(request, pk, feedback):
    comment = get_object_or_404(Comment, pk=pk)
    comment.set_feedback(feedback)
    return redirect("products:product_detail", pk=comment.product.pk)

@login_required
def comment_toggle_hidden(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user == comment.user or request.user.is_staff:
        comment.toggle_hidden_status()
        return redirect("products:product_detail", pk=comment.product.pk)
    else:
        return redirect("products:product_detail", pk=comment.product.pk)