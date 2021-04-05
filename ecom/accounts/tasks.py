from __future__ import absolute_import, unicode_literals
from django.core.mail import send_mail
from celery import shared_task
from time import sleep


@shared_task
def sleepy(duration):
    sleep(duration)
    return None


@shared_task
def sent_mail(email):
    sleep(10)
    send_mail("hello", "How ARE you", 'ridhamdata@gmail.com',[email])
    return None
