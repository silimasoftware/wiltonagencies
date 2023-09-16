from django import forms
from .models import Product, ProductImage, ProductCategory


# Create the form class.
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', "description", "country"]


class ProductImageForm(forms.ModelForm):
    upload = forms.ImageField(widget=forms.widgets.ClearableFileInput(attrs={'multiple':True}))
    class Meta:
        model = ProductImage
        fields = ["name", "upload"]


class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ["name", "description", "product"]

