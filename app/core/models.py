from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from utils.constants import StatusType, DomainsType

from enumchoicefield import EnumChoiceField


class UserManager(BaseUserManager):
    """Custom Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create a user using the custom manager."""
        if not email:
            raise ValueError('User must have an email!')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        """Create a user using the custom manager."""
        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class BaseModel(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    deleted_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Forest(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500, unique=True)
    domain = EnumChoiceField(enum_class=DomainsType)
    status = EnumChoiceField(enum_class=StatusType,
                             default=StatusType.active)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
