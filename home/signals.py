from django.dispatch import receiver
from django.db.models.signals import post_save
from accounts.models import User
from rest_framework.authtoken.models import Token
from accounts.views import CreateUserView


@receiver(post_save, sender=User)
def create_auth_token(instance=None, created=False, **kwargs):
    if created:
        token = Token.objects.create(user=instance)
        if CreateUserView.allow_send:
            return CreateUserView.get_token({'token': token.key})
        else:
            token
