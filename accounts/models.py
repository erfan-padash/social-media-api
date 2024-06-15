from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import MyUserManager


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(verbose_name='phone_number',
                                    max_length=11,
                                    unique=True)
    email = models.EmailField(verbose_name='email',
                              max_length=250,
                              unique=True)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'phone_number'

    REQUIRED_FIELDS = ['email', 'full_name']

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return f'{self.id}'

    def get_token(self):
        return self.auth_token

    def get_count_account(self):
        return self.auser.count()


class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='auser')
    profile_image = models.ImageField(upload_to='Account/')
    account_name = models.CharField(max_length=200, unique=True)
    bio = models.CharField(max_length=200, default='hi i am a user', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.account_name[:15]

    def all_post(self):
        return self.paccount.all()
