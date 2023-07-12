from django import forms
from .models import Comment, Rating


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]

    text = forms.CharField(
        label=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control comment-text",
                "placeholder": "Füge dein Kommentar hinzu...",
                "rows": "4",
                "cols": "50",
            }
        )
    )

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["rating"]

    rating = forms.IntegerField(
        label=False,
        min_value=0,
        max_value=5,
        widget=forms.NumberInput(attrs={"class": "form-control rating-number"}),
    )
