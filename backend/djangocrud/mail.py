from django.core.mail import send_mail
from djangocrud.models import Subscriber, Post

send_mail(
    'Subject here',
    'Here is the message.',
    'from@example.com',
    ['to@example.com'],
    fail_silently=False,
)