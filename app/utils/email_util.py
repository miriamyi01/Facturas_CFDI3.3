# services/email_service.py

"""
Este archivo define una función para enviar correos electrónicos con archivos adjuntos.
"""

from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def enviar_correo(correo_destino, archivo):
    """
    Envía un correo electrónico con un archivo adjunto.

    Args:
        correo_destino (str): La dirección de correo electrónico del destinatario.
        archivo (file): El archivo a adjuntar al correo.

    Returns:
        None
    """
    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = 'prueba@gmail.com'
    msg['To'] = correo_destino
    msg['Subject'] = 'El asunto de tu correo'

    # Agregar el cuerpo del correo
    body = 'El cuerpo de tu correo'
    msg.attach(MIMEText(body, 'plain'))

    # Adjuntar el archivo PDF
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(archivo.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="Factura.pdf"')
    msg.attach(part)

    # Iniciar sesión en el servidor
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # Ingresar las credenciales para el correo electrónico
    server.login(msg['From'], 'tu_contraseña')

    # Enviar el correo
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()