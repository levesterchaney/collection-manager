from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CollectionItem


@receiver(post_save, sender=CollectionItem)
def schedule_value_estimation(sender, instance, created, **kwargs):
    if not created:
        return

    from django_q.tasks import async_task
    async_task(
        'apps.collections.tasks.estimate_item_value',
        instance.pk,
        task_name=f"value-estimate-{instance.pk}",
    )