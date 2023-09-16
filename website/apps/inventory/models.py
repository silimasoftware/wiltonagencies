import os
from django.db import models
from django_countries.fields import CountryField

class BaseProduct(models.Model):
    uid = models.CharField(max_length=64, default="0")
    active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ["created"]

    def __str__(self):
        return self.uid


class Product(BaseProduct):
    name = models.CharField(max_length=128)
    product_code = models.CharField(max_length=128)
    description = models.TextField()
    country = CountryField()
    net_weight = models.FloatField()
    net_weight_unit = models.CharField(max_length=128)
    gross_weight = models.FloatField()
    gross_weight_unit = models.CharField(max_length=128)

    def __str__(self):
        return self.name



class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    name = models.CharField(max_length=128)

    def _path(self, filename):
        return os.path.join("products", self.product.uid, filename)
    
    upload =  models.ImageField(upload_to=_path)
    
    def __str__(self):
        return self.name



class ProductCategory(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    product = models.ManyToManyField(Product)
    
    def __str__(self):
        return self.name
