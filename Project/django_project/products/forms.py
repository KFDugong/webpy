from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-field'}), label="Name")
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control my-field'}), label="Beschreibung")
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control my-field'}), label="Preis")
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file my-field'}), label="Bild")
    manual = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control-file my-field'}), label="Bedienungsanleitung")

    class Meta:
        model = Product
        fields = ["name", "description", "price", "image", "manual"]
