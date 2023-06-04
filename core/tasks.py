
from django.core.mail import EmailMessage, get_connection
from django.conf import settings

import os
from celery import shared_task
from social_list.celery import app


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

@shared_task
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

