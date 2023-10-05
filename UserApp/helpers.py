from django.core.mail import send_mail
import uuid


def send_forget_password_mail(email):
    token = str(uuid.uuid4())
    subject ='your forget password link'
    message = f'Click on the link to reset your password'

