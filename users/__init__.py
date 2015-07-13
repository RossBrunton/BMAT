""" This module contains methods for interacting with a user's account, such as logging in and changing settings """
from django.contrib.auth.models import User
from django.core.exceptions import SuspiciousOperation, ValidationError
from django.utils.timezone import UTC

import random
from datetime import datetime, timedelta

def _randstr(n):
    """ Returns a random string """
    return ''.join(random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(n))

def make_trial_user():
    """ Creates a new user with a random username, no password or email with settings.is_trial set to True """
    c = 0
    
    while c < 20:
        c += 1
        uid = _randstr(5)
        
        try:
            User.objects.get(username="trial_"+uid)
        except User.DoesNotExist:
            # Unused uid, create one
            user = User.objects.create_user("trial_"+uid)
            
            user.settings.is_trial = True
            user.settings.save()
            
            return user
    
    raise SuspiciousOperation


def clean_trial():
    """ Deletes trial accounts more than 2 days old """
    User.objects.filter(date_joined__lt=datetime.now(UTC())-timedelta(days=2), settings__is_trial=True).delete()
