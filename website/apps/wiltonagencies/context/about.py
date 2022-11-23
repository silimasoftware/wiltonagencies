from wiltonagencies.util import (
    get_msgs,
    send_mail,
    SMTPException,
    time,
    push_msg,
    is_post,
    is_get,
    bleach,
)


def about_context(request):
    if is_get(request):
        return {"page_title": "About Us"}