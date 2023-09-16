from inventory.models import Product, ProductImage
from inventory.forms import ProductForm
from core.util import Callable


class ProductContext(Callable):
    @staticmethod
    def index(portal: object) -> dict:
        products = []
        qs = Product.objects.all()
        for p in qs:
            images = ProductImage.objects.filter(product__uid=p.uid)
            product = {
                "country": p.country,
                "name": p.name,
                "images": images,
                "description": p.description,
                "uid": p.uid,
            }
            products.append(product)
        return {
            "tag": "save_product",
            "products": products,
        }
