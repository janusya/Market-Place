from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email')
        if not name:
            raise ValueError('Users must have a name')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
        )
        user.create_activation_code()
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    register_date = models.DateTimeField(null=True, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    activation_code = models.CharField(
        max_length=25,
        blank=True
    )
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def create_activation_code(self):
        from django.utils.crypto import get_random_string

        code = get_random_string(
            length=25
        )

        self.activation_code = code

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):

        if not self.register_date:
            self.register_date = datetime.now()

        super(User, self).save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_superuser
