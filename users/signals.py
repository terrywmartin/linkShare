from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings
from .models import UserProfile ,User

def create_update_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = UserProfile.objects.create(user = user)


post_save.connect(create_update_profile, sender=User)




