import json
import uuid
import bleach
import secrets
from django.views import View
from smtplib import SMTPException
from django.http import HttpResponse, HttpResponseForbidden
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
import logging


logger = logging.getLogger("website_logger")


def push_msg(request, msg, tag):
    messages.add_message(request, messages.INFO, msg, extra_tags=tag)


def get_msgs(request):
    return render_to_string(
        "src/msgs.html",
        {"msg": get_messages(request)},
        request,
    )


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
