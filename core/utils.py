
from django.core.mail import EmailMessage, get_connection
from django.conf import settings

import os

import qrcode
import qrcode.image.svg

from io import BytesIO


def generate_qr_code(url):
    factory = qrcode.image.svg.SvgImage
    qr = qrcode.QRCode(
             version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=20,
            border=4,
            image_factory=factory
        )
    
    qr.add_data(url)
    img = qr.make_image(fill_color="black", back_color="white")
    stream = BytesIO()
    img.save(stream) 
    return stream

def get_email_connection():
 use_tls = True
 use_ssl = False
 fail_silently=False
 connection = get_connection(host=settings.EMAIL_HOST, 
                        port=settings.EMAIL_PORT, 
                        username=settings.EMAIL_HOST_USER, 
                        password=settings.EMAIL_HOST_PASSWORD, 
                        use_tls=use_tls,
                        use_ssl=use_ssl,
            fail_silently=fail_silently)
 return connection

def email_user(email_address, html, subject=None):
    #email_username = str(os.getenv('EMAIL_USERNAME'))
    #email_password = str(os.getenv('EMAIL_PASSWORD'))
    from_email = str(os.getenv('FROM_EMAIL'))
    
    success = { 'result': 0, 'message': ''}
    try:
            if not subject:
                subject = "Secret Share Invitation"
            connection = get_email_connection()
            email = EmailMessage(subject,html, from_email, [email_address],connection=connection)
            email.content_subtype = 'html'
            resp = email.send(fail_silently=False)

            success['result']=resp

    except Exception as ex:
            success['result'] = 0
            success['message'] = ex 
    
    return success

