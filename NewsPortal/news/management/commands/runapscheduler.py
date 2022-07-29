import logging
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import *


logger = logging.getLogger(__name__)


def my_job():
    for cat in Category.objects.all():
        for sub in UserCategory.objects.filter(category=cat):
            post = PostCategory.objects.filter(categoryThrough=cat)
            msg = EmailMultiAlternatives(
                subject=f'Публикации за неделю в категории новостей {cat}',
                from_email='*****@yandex.ru'
            )
            html_content = render_to_string(
                'week_sender.html',
                {
                    'post': post,
                    'sub': sub,
                }
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


