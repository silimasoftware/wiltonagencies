from .util import (
    HttpResponse,
    SMTPException,
    View,
    bleach,
    json,
    is_ajax,
    is_get,
    is_post,
    render,
    logger,
    render,
    messages,
    time,
    send_mail,
    get_msgs,
    forbidden,
)
from .context import get_context


def under_construction_view(request):
    if is_post(request):
        return forbidden()
    if is_get(request):
        request.context = {
            "javascript": [
                f"js/home.js",
            ],
        }
        return render(request, "under_construction.html", request.context)

def contact_view(request):
    if is_post(request):
        return forbidden()
    if is_get(request):
        return render(request, "contact.html")



def page_loader_view(request, page="home", function="index"):
    request.page = bleach.clean(page)
    request.function = bleach.clean(function)
    request.template_path = f"pages/{request.page}/index.html"
    request.javascript_path = f"js/{request.page}.js"
    if request.POST.get("action"):
        request.action = bleach.clean(request.POST.get("action"))
    else:
        request.action = request.page

    if is_post(request):
        try:
            get_context(request)
        except Exception as e:
            logger.exception(e)
            return HttpResponse(
                json.dumps({"Failed to proccess the request!"}),
                content_type="application/json",
            )

        return HttpResponse(
            json.dumps(request.context), content_type="application/json"
        )

    if is_get(request):
        try:
            get_context(request)
        except Exception as e:
            logger.exception(e)
            return page_not_found_view(request, e)

        return render(request, "index.html", request.context)


def page_not_found_view(request, exception):
    messages.error(
        request,
        message="Failed to find the page or resource!",
        extra_tags="warning",
    )
    return render(request, "index.html", {"template": "src/404.html"}, status=404)
