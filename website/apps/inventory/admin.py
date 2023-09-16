from django.contrib import admin
from .models import Product, ProductImage, ProductCategory


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass