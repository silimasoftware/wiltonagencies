import uuid
from core.util import get_object_or_404, render_to_string, Callable
from inventory.forms import ProductForm, ProductImageForm
from inventory.models import Product, ProductImage
from portal.context import ProductContext
from core.util import debug, deserialize_form, bleach


class ProductAjax(Callable):
    @staticmethod
    def product_form(portal: object) -> dict:
        page = render_to_string(
            "portal/products/add_product.html",
            {
                "tag": "save_product",
                "product_form": ProductForm(),
            },
            portal.request,
        )
        return {
            "modal": page,
        }

    @staticmethod
    def edit_product(portal: object) -> dict:
        product = get_object_or_404(Product, uid=portal.uid)
        _form = ProductForm(instance=product)
        page = render_to_string(
            "portal/products/add_product.html",
            {
                "uid": portal.uid,
                "tag": "update_product",
                "product_form": _form,
            },
            portal.request,
        )
        return {
            "modal": page,
        }

    @staticmethod
    def save_product(portal: object) -> dict:
        _form = ProductForm(portal.request.POST)
        if _form.is_valid():
            _name = _form.cleaned_data.get("name").replace("%20", " ")
            _description = (
                _form.cleaned_data.get("description")
                .replace("%20", " ")
                .replace("%0D%0A", "<br>")
            )
            _country = _form.cleaned_data.get("country")
            _net_weight =  0 #_form.cleaned_data.get("net_weight")
            _net_weight_unit = "kg" #_form.cleaned_data.get("net_weight_unit")
            _gross_weight = 0 #_form.cleaned_data.get("gross_weight")
            _gross_weight_unit = "kg" #_form.cleaned_data.get("gross_weight_unit")
            _product = Product(
                uid=uuid.uuid4(),
                product_code=uuid.uuid4(),
                name=_name,
                description=_description,
                country=_country,
                net_weight=_net_weight,
                net_weight_unit=_net_weight_unit,
                gross_weight=_gross_weight,
                gross_weight_unit=_gross_weight_unit,
            )
            _product.save()
            page = render_to_string(
                "portal/products/index.html",
                ProductContext.index(portal),
                portal.request,
            )
            return {
                "html": page,
            }
        else:
            return ProductAjax.edit_product(portal)

    @staticmethod
    def update_product(portal: object) -> dict:
        product = get_object_or_404(Product, uid=portal.uid)
        _form = ProductForm(portal.request.POST, instance=product)
        if _form.is_valid():
            # save_it = _form.save(commit=False)
            _form.save()
            page = render_to_string(
                "portal/products/index.html",
                ProductContext.index(portal),
                portal.request,
            )
            return {
                "html": page,
            }
        else:
            return ProductAjax.edit_product(portal)

    @staticmethod
    def product_image_form(portal: object) -> dict:
        page = render_to_string(
            "portal/products/add_image.html",
            {
                "puid": portal.uid,
                "product_image_form": ProductImageForm(),
            },
            portal.request,
        )
        return {
            "modal": page,
        }

    @staticmethod
    def save_product_image(portal: object) -> dict:
        try:
            _form = ProductImageForm(portal.request.POST, portal.request.FILES)
            if _form.is_valid():
                _name = _form.cleaned_data.get("name")
                _images = portal.request.FILES.getlist("upload")
                _product = get_object_or_404(Product, uid=portal.uid)
                for i in _images:
                    pi = ProductImage(product=_product, name=_name, upload=i)
                    print(pi)
                    pi.save()
            else:
                print("FAILED")

        except Exception as e:
            debug(request=portal.request, log=True, msg=e)

        page = render_to_string(
            "portal/products/index.html",
            ProductContext.index(portal),
            portal.request,
        )
        return {
            "html": page,
        }
