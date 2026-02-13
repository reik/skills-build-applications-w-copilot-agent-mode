from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile when a new User is created"""
    if created:
        try:
            UserProfile.objects.create(user=instance)
        except Exception as e:
            # Silently handle errors to prevent registration failures
            # This can happen due to Djongo/ObjectId issues
            pass


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the UserProfile when the User is saved"""
    try:
        if hasattr(instance, 'profile'):
            instance.profile.save()
    except Exception:
        # Silently handle errors
        pass
