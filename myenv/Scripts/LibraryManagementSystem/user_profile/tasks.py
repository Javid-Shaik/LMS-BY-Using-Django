# user_profile/tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_book_available_notification(book_title, user_email):
    subject = 'Book Available Notification'
    message = f'The book "{book_title}" is now available in our library.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
