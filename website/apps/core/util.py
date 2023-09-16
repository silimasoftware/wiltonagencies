import logging
import json
import uuid
import bleach
from django.views import View
from smtplib import SMTPException
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.template import RequestContext
from django.template import TemplateDoesNotExist
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.template.loader import get_template, render_to_string
from django.contrib.messages import get_messages
from django.core.mail import send_mail
from django.contrib import messages
from datetime import datetime
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


logger = logging.getLogger("file_logger")


class Callable(object):
    """
    Magic
    """

    def __call__(self: object, cls: object) -> dict:
        return getattr(self, cls.action)(cls)


class AuthRequired(object):
    """
    Mixin method decorator to check user is authenticated
    """

    @method_decorator(login_required(login_url="/backend/login/"))
    def dispatch(self, request, *args, **kwargs):
        return super(AuthRequired, self).dispatch(request, *args, **kwargs)


class StaffRequired(object):
    """
    Mixin method decorators to check user is authenticated & staff
    """

    @method_decorator(login_required(login_url="/backend/login/"))
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffRequired, self).dispatch(request, *args, **kwargs)


def get_msgs(request):
    return render_to_string(
        "src/msgs.html",
        {"msg": get_messages(request)},
        request,
    )


def debug(request, pop=False, msg=None, tag=None, log=False, e=None):
    if pop is True and msg is not None:
        messages.info(
            request,
            message=f"{time()} : {msg}",
            extra_tags=f"{tag}",
        )
    if log is True and e is not None:
        logger.exception(e)


def is_ajax(request):
    return (
        True if request.headers.get("x-requested-with") == "XMLHttpRequest" else False
    )


def is_post(request):
    return True if request.method == "POST" else False


def is_get(request):
    return True if request.method == "GET" else False


def forbidden():
    return HttpResponseForbidden()


def time():
    now = datetime.now()
    return now.strftime("%y/%m/%d %H:%M:%S.%f")


def deserialize_form(data):
    return dict(i.split("=") for i in data.split("&"))


def send_contact_mail(request):
    name = bleach.clean(request.POST.get("name"))
    email = bleach.clean(request.POST.get("email"))
    subject = bleach.clean(request.POST.get("subject"))
    message = bleach.clean(request.POST.get("message"))
    try:
        send_mail(
            f"Message from Name:[{name}] Email:[{email}] Regarding:[{subject}]",
            f"{message}",
            "noreply@silimasoftware.com",
            ["contact@silimasoftware.com"],
        )
    except SMTPException as e:
        messages.error(
            request,
            message=f"{time()} ERROR: {e} ",
            extra_tags="danger",
        )
        return {"msg_list": get_msgs(request)}
    else:
        # submit counter
        if "support_mail_sent" in request.session:
            request.session["support_mail_sent"] += 1
        else:
            request.session["support_mail_sent"] = 1

        return {"success": "True"}
