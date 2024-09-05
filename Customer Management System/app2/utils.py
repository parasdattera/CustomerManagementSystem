from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings






def send_password_reset_email(email, token):
    subject = 'Password Reset Request'
    message = f'Click the following link to reset your password:\n\nReset Link: http://127.0.0.1:8000/reset-password/{token}/'
    from_email = 'parasdattera555@gmail.com'  # Replace with your email
    recipient_list = [email]

    email = EmailMessage(subject, message, from_email, recipient_list)
    email.send()