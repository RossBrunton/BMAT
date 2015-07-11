""" Extra models for users, only contains the settings model at the moment """

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Settings(models.Model):
    """ Additional user settings, this is attached to a user when they are created
    
    It has the following fields:
    - user:OneToOneField
    - theme:CharField
    
    At the moment theme can be either Settings.THEME_GREY_BOXES or Settings.THEME_LIGHT, with the default being light.
    A list of all these themes as (constant, pretty name) are available as Settings.THEME_OPTIONS.
    """
    THEME_GREY_BOXES = "grey_boxes"
    THEME_LIGHT = "light"
    
    THEME_OPTIONS = (
        (THEME_GREY_BOXES, "Grey Boxes"),
        (THEME_LIGHT, "Light")
    )
    
    URL_SETTINGS_VALIDATE = "v"
    URL_SETTINGS_NOLINK = "n"
    URL_SETTINGS_LINK = "y"
    
    URL_SETTINGS = (
        (URL_SETTINGS_VALIDATE, "Check if URLs are correct"),
        (URL_SETTINGS_NOLINK, "Allow incorrect URLs"),
        (URL_SETTINGS_LINK, "Allow incorrect URLs, and make them links")
    )
    
    user = models.OneToOneField(User, unique=True)
    theme = models.CharField(max_length=10, default=THEME_LIGHT, choices=THEME_OPTIONS)
    url_settings = models.CharField(max_length=1, default=URL_SETTINGS_VALIDATE, choices=URL_SETTINGS)
    no_analytics = models.BooleanField(default=False)
    
    def __str__(self):
        return ("Settings for "+self.user.username).encode("ascii", "ignore").decode("ascii")


@receiver(post_save, sender=User)
def _add_settings(sender, instance, **kwargs):
    """ When a user is saved and has no settings, add it """
    try:
        instance.settings
    except ObjectDoesNotExist:
        instance.settings = Settings.objects.create(user=instance)
