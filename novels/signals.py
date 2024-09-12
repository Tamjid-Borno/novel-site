# novels/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create the user profile if the user is newly created
        UserProfile.objects.create(user=instance)
    else:
        # Save the user profile if the user is being updated
        instance.userprofile.save()
