from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from panel.models import Messages, Setting

@receiver(post_save, sender=Messages)
def update_unread_messages(sender, instance, created, **kwargs):
    print('update_unread_messages:')
    print(sender, instance, created)
    setting = Setting.objects.get(id=1)
    if created and instance.status == 'OPEN':
        if setting.total_unread_messages is not None:
            setting.total_unread_messages += 1
        else:
            setting.total_unread_messages = 0
        setting.save()
    if not created and instance.status == 'CLOSED':
        setting.total_unread_messages -= 1
        setting.save()

    print(setting.total_unread_messages)