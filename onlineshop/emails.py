from django.core.mail import send_mail
from .models import EmailAddress

def send_email_to_selected(emails):
    send_mail(
        'Tiêu đề Email',
        'Nội dung Email.',
        'từ@example.com',
        emails,
        fail_silently=False,
    )
