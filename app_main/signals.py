import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.db.models.signals import post_save
from django.dispatch import receiver

from app_main.models import Product, Suscriptor
from gaia import settings


@receiver(post_save, sender=Product)
def save_hash(sender, instance: Product, created, **kwargs):
    prod = instance
    if created:
        if Suscriptor.objects.exists():
            remitente = settings.EMAIL_HOST_USER
            destinatarios = [i.email for i in Suscriptor.objects.all()]
            asunto = 'Nuevo producto disponible'
            cuerpo = f'Nombre: {prod.name}\nPrecio: {prod.price}\Tiempo de entrega: {prod.delivery_time}\n'
            ruta_adjunto = prod.image.path
            nombre_adjunto = f'{prod.name}.jpg'
            # Creamos el objeto mensaje
            mensaje = MIMEMultipart()
            # Establecemos los atributos del mensaje
            mensaje['From'] = remitente
            mensaje['BCC'] = ", ".join(destinatarios)
            mensaje['Subject'] = asunto
            # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
            mensaje.attach(MIMEText(cuerpo, 'plain'))
            # Abrimos el archivo que vamos a adjuntar
            archivo_adjunto = open(ruta_adjunto, 'rb')
            # Creamos un objeto MIME base
            adjunto_MIME = MIMEBase('application', 'octet-stream')
            # Y le cargamos el archivo adjunto
            adjunto_MIME.set_payload((archivo_adjunto).read())
            # Codificamos el objeto en BASE64
            encoders.encode_base64(adjunto_MIME)
            # Agregamos una cabecera al objeto
            adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % nombre_adjunto)
            # Y finalmente lo agregamos al mensaje
            mensaje.attach(adjunto_MIME)
            # Creamos la conexión con el servidor
            sesion_smtp = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            # Ciframos la conexión
            sesion_smtp.starttls()
            # Iniciamos sesión en el servidor
            sesion_smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            # Convertimos el objeto mensaje a texto
            texto = mensaje.as_string()
            # Enviamos el mensaje
            sesion_smtp.sendmail(remitente, destinatarios, texto)
            # Cerramos la conexión
            sesion_smtp.quit()
            print('se envio el correo')
    # else:
    #     print(os.path.join(os.getcwd(),settings.BASE_DIR, str(prod.get_image())))
    #     print(prod.image.path)
