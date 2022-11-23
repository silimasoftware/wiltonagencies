from wiltonagencies.util import (
    is_get,

)


def product_context(request):
    if is_get(request):
        return {"page_title": "Export, Import, Consulting, International Trade"}