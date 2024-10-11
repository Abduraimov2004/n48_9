from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Post


@receiver(post_save, sender=Post)
def post_save_handler(sender, instance, created, **kwargs):
    if created:
        print(f"Post created: {instance.title}")
    else:
        print(f"Post updated: {instance.title}")


@receiver(post_delete, sender=Post)
def post_delete_handler(sender, instance, **kwargs):
    print(f"Post deleted: {instance.title}")
