from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Project, Task, ActivityLog
from .middleware import get_current_user

def log_activity(sender, instance, action, **kwargs):
    user = get_current_user()
    if user and not user.is_authenticated:
        user = None
    
    ActivityLog.objects.create(
        user=user,
        action=action,
        model_name=sender.__name__,
        object_id=str(instance.pk)
    )

@receiver(post_save, sender=Project)
@receiver(post_save, sender=Task)
def log_save_activity(sender, instance, created, **kwargs):
    action = 'CREATE' if created else 'UPDATE'
    # For soft delete on Task, if is_deleted changed to True, we could log it as DELETE
    # But since the requirement says "UPDATE" for changes and "DELETE" for real deletes,
    # we log UPDATE here, and we can also check if it's a soft-delete.
    if isinstance(instance, Task) and instance.is_deleted and not created:
        action = 'DELETE'
    log_activity(sender, instance, action)

@receiver(post_delete, sender=Project)
@receiver(post_delete, sender=Task)
def log_delete_activity(sender, instance, **kwargs):
    # This covers hard deletes
    log_activity(sender, instance, 'DELETE')
