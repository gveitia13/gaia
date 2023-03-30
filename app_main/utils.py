from django.http import HttpRequest

from gaia import settings


def get_host_url(request: HttpRequest) -> str:
    if request.get_host().__contains__("127.0.0.1") or request.get_host().__contains__(
            "localhost"):
        host = 'http://'
    else:
        host = 'https://'
    return host


def get_full_URL(request: HttpRequest) -> str:
    from django.contrib.sites.shortcuts import get_current_site
    current_site = get_current_site(request)
    host = get_host_url(request) + current_site.domain
    return host


def create_mail(to, subject, template_name, context, attached_file=None):
    from django.template.loader import get_template
    template = get_template(template_name)
    content = template.render(context)

    from django.core.mail import EmailMultiAlternatives
    message = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=[to],
        cc=[]
    )
    message.attach_alternative(content, 'text/html')
    if attached_file:
        message.attach_file(attached_file)
    return message


# mail = create_mail('pasar parametros')
# mail.send(fail_silently=False)
colors = (
    ('198754', 'Verde'),
    ('ffc107', 'Amarillo'),
    ('8cbf44', 'Verde Claro'),
    ('fd7e14', 'Anaranjado'),
    ('dc3545', 'Rojo'),
    ('6c757d', 'Gris'),
    ('0d6efd', 'Azul'),
)


def validate_only_numbers(value):
    if not value.isdigit():
        from django.core.exceptions import ValidationError
        raise ValidationError('Este campo solo acepta números.')
