import imp
from .contact import contact_context
from .about import about_context
from .home import home_context
from .blog import blog_context
from .partner import partner_context
from .product import product_context

def get_context(request):
    request.context = {
        "current_page": request.path.split("/")[-2],
        "page": request.page,
        "function": request.function,
        "template": request.template_path,
        "javascript": [
            request.javascript_path,
        ],
    }
    try:
        _page = context_factory(request)
    except Exception as e:
        raise e
    else:
        request.context |= _page if _page else no_context()


def context_factory(request):
    func = {
        "home": home_context,
        "partners": partner_context,
        "products": product_context,
        "blog": blog_context,
        "about": about_context,
        "contact": contact_context,
    }
    return func[request.page](request)


def no_context(*args, **kwargs):
    return {}
