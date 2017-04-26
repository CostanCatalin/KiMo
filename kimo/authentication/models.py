from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username')

        account = self.model(email=self.normalize_email(email), username=kwargs.get('username'))
        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)

        account.is_superuser = True
        account.is_staff = True
        account.save()

        return account


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)

    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([str(self.first_name), str(self.last_name)])

    def get_short_name(self):
        return self.first_name


class AccountProfile(models.Model):
    user = models.OneToOneField(Account)
    birth_date = models.DateField(null=True)
    phone_number = models.CharField(max_length=40, null=True)
    country = models.CharField(max_length=40, null=True)
    region = models.CharField(max_length=40, null=True)
    street_name = models.CharField(max_length=40, null=True)
    street_number = models.IntegerField(null=True)
    kids = models.IntegerField(default=0)

    def __unicode__(self):
        return u'<' + self.user.email + u' Profile>'









