from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Settings(models.Model):
    user = models.OneToOneField(User, unique=True)
    
    def __str__(self):
        return "Settings for "+self.user.username


@receiver(post_save, sender=User)
def _add_settings(sender, instance, **kwargs):
    try:
        instance.settings
    except ObjectDoesNotExist:
        instance.settings = Settings.objects.create(user=instance)
