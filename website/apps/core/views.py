import json
from django.contrib import auth
from .util import (
    debug,
    bleach,
    JsonResponse,
    HttpResponse,
    HttpResponseForbidden,
    render,
    redirect,
    is_ajax,
    AuthRequired,
)
from .models import Link
from django.views import View
from portal.context import DefaultContext, ProductContext
from portal.ajax import DefaultAjax, ProductAjax


class ContextManager(View):
    def dispatch(self, request, module="core", page="index"):
        self.module = bleach.clean(module)
        self.page = bleach.clean(page)
        self.request = request

        if request.POST.get("action"):
            self.action = bleach.clean(request.POST.get("action"))
        else:
            self.action = page

        if request.POST.get("tag"):
            self.tag = bleach.clean(request.POST.get("tag"))
        else:
            self.tag = None

        if request.POST.get("uid"):
            self.uid = bleach.clean(request.POST.get("uid"))
        else:
            self.uid = None

        self.context = {
            "current_page": request.path.split("/")[-2],
            "app": "portal",
            "module": self.module,
            "page": self.page,
            "app_path": f"portal/index.html",
            "module_path": f"portal/{self.module}/{self.page}.html",
            "main_nav": Link.objects.filter(nav__name__contains="portal"),
            "module_nav": Link.objects.filter(nav__name__contains=self.module),
            "page_nav": Link.objects.filter(nav__name__contains=self.page),
            "javascript": [
                "js/htmx.js",
                "js/jq.js",
                "js/popper.js",
                "js/bs.js",
                f"js/portal/{self.module}.js",
            ],
            "css": [
                "css/bs.css",
                "css/main.css",
            ],
        }
        return super(ContextManager, self).dispatch(request)

    def pass_context(*args, **kwargs) -> None:
        pass

    def no_context(*args, **kwargs) -> dict:
        return {}


class Portal(AuthRequired, ContextManager):
    def post(self, request):
        if not is_ajax(request):
            return JsonResponse({"error": "nope..."})

        ajax_modules = {
            "core": DefaultAjax,
            "clients": DefaultContext,
            "leads": DefaultContext,
            "products": ProductAjax,
        }
        try:
            ctx = ajax_modules[self.module]()(self)
        except Exception as e:
            debug(request, log=True, e=e)
            return JsonResponse({"error": e})
        else:
            debug(request, log=True, e=ctx)
            return HttpResponse(json.dumps(ctx), content_type="application/json")

    def get(self, request):
        get_modules = {
            "core": DefaultContext,
            "clients": DefaultContext,
            "leads": DefaultContext,
            "products": ProductContext,
        }
        try:
            ctx = get_modules[self.module]()(self)
        except Exception as e:
            debug(request, log=True, e=e)
            return render(request, "src/404.html", self.context)
        else:
            self.context |= ctx if ctx else self.no_context()
            return render(request, "portal/index.html", self.context)


class Logout(AuthRequired, ContextManager):
    def post(self, request):
        request.session["user_token"] = "0"
        self.context["javascript"].append("js/auth/logout.js")
        auth.logout(request)
        return render(request, "src/logout.html", self.context)

    def get(self, request):
        return HttpResponseForbidden(request)


class Login(ContextManager):
    def post(self, request):
        user = auth.authenticate(
            username=request.POST["email"], password=request.POST["password"]
        )
        if user is not None:
            auth.login(request, user)
            next = request.session.pop("next")
            return redirect(next)
        else:
            debug(request, pop=True, msg="O_O")
            return render(request, "src/login.html", self.context)

    def get(self, request):
        if "next" in request.GET:
            request.session["next"] = request.GET["next"]
        else:
            request.session["next"] = "/"

        return render(request, "src/login.html", self.context)


def page_not_found_view(request, exception):
    context = {"template": "src/404.html"}
    return render(request, "portal/index.html", context, status=404)


def page_error_view(request):
    context = {"template": "src/500.html"}
    return render(request, "portal/index.html", context, status=500)
