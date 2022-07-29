from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import EmailMultiAlternatives  # импортируем класс для создание объекта письма с html
from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
from .models import Post, PostCategory, UserCategory


@receiver(m2m_changed, sender=PostCategory)
def notify_post_create(sender, instance, action, **kwargs):
    if action == 'post_add':
        for cat in instance.postCategory.all():
            for subscribe in UserCategory.objects.filter(category=cat):
                msg = EmailMultiAlternatives(
                    subject=instance.title,
                    body=instance.text,
                    from_email='*****@yandex.ru',
                    to=[subscribe.user.email],
                )
                html_content = render_to_string(
                    'flatpages/subscribemessage.html',
                    {
                        'post': instance.title,
                        'recipient': subscribe.user.email,
                    },
                )

                msg.attach_alternative(html_content, "text/html")
                msg.send()
