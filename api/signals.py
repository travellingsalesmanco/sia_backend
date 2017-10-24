from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token

from . import models

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def on_user_creation(sender, instance, created, **kwargs):
    # If user is newly created
    if created:
        # Create a profile for the user
        models.Profile.objects.create(user=instance)
        # Create a Token for the user
        Token.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def on_user_update(sender, instance, **kwargs):
    # Also update user profile
    instance.profile.save()
