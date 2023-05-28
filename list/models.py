from django.db import models

import uuid

from users.models import User

# Create your models here.
class Link(models.Model):
    SOCIAL_LINKS = (
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('tiktok', 'TikTok'),
        ('linkedin', 'LinkedIn'),
        ('github', 'GitHub'),
        ('discord', 'Discord'),
        ('youtube', 'YouTube'),
        ('medium', 'Medium'),
        ('telegram', 'Telegram'),
        ('etsy', 'Etsy'),
        ('twitch', 'Twitch'),
        ('reddit', 'Reddit'),
        ('patreon', 'Patreon'),
        ('flickr', 'Flickr'),
        ('other', 'Other'),

    )

    id = models.UUIDField(primary_key=True, editable=False,default=uuid.uuid4)
    handle = models.CharField(max_length=100,null=False, blank=False)
    link = models.CharField(max_length=200,blank=True,null=True)
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    type = models.CharField(choices=SOCIAL_LINKS,max_length=100)

    def __str__(self):
        return self.handle
    

