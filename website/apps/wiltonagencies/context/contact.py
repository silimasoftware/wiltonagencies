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


def contact_context(request):
    if is_get(request):
        return {"page_title": "Contact Us"}
    if is_post(request):
        name = bleach.clean(request.POST.get("name"))
        email = bleach.clean(request.POST.get("email"))
        subject = bleach.clean(request.POST.get("subject"))
        message = bleach.clean(request.POST.get("message"))
        try:
            send_mail(
                f"Message from Name:[{name}] Email:[{email}] Regarding:[{subject}]",
                f"{message}",
                "noreply@wiltonagencies.com",
                ["contact@wiltonagencies.com"],
            )
        except SMTPException as e:
            push_msg(
                request,
                f"{time()} ERROR: {e} ",
                "danger",
            )
            return {"msg_list": get_msgs(request)}
        else:
            # submit counter
            if "support_mail_sent" in request.session:
                request.session["support_mail_sent"] += 1
            else:
                request.session["support_mail_sent"] = 1

            return {"success": "True"}
