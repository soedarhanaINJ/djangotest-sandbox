import os
from typing import Any, Tuple

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django_q.tasks import async_task


def open_template(template_path: str) -> str:
    if not os.path.isfile(template_path):
        raise FileNotFoundError(f"Template {template_path} not found.")

    content: str
    with open(template_path, "r") as fp:
        content = fp.read()

    return content


def compose_html_content(
    appname: str, template_name: str, **kwargs: Any
) -> Tuple[str, str]:
    base_path = os.path.join(settings.BASE_DIR, appname, "mail_templates")

    text_path = os.path.join(base_path, "text", f"{template_name}.txt")
    text_code = open_template(text_path)

    html_path = os.path.join(base_path, "html", f"{template_name}.html")
    html_code = open_template(html_path)

    for key, value in kwargs.items():
        keyname = "__" + key + "__"
        text_code = text_code.replace(keyname, value)
        html_code = html_code.replace(keyname, value)

    return html_code, text_code


def execute_sending_email(
    subject: str, html_content: str, text_content: str, receiver: str
) -> None:
    email = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER, [receiver]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()


def send_html_mail(
    appname: str,
    subject: str,
    template_name: str,
    receiver: str,
    **kwargs: Any,
) -> None:
    html_content, text_content = compose_html_content(
        appname, template_name, **kwargs
    )

    if not settings.SEND_EMAIL:
        print(text_content)
        return

    async_task(
        execute_sending_email, subject, html_content, text_content, receiver
    )
