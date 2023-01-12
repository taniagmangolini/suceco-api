from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from utils.constants import DomainType, StageType, StateType

from enumfields import EnumIntegerField


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
    """Base model for all models."""

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    deleted_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    """User model."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Forest(BaseModel):
    """Forest model."""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500, unique=True)
    domain = EnumIntegerField(enum=DomainType)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Reference(BaseModel):
    """Reference model."""

    id = models.AutoField(primary_key=True)
    publication = models.CharField(max_length=1000, default='', unique=True)
    url = models.CharField(max_length=1000, default='')

    def __str__(self):
        return '-'.join([str(self.id), self.publication, self.url])


class Species(BaseModel):
    """Species model."""

    id = models.AutoField(primary_key=True)
    scientific_name = models.CharField(max_length=1000,
                                       unique=True,
                                       help_text='Species')

    def __str__(self):
        return self.scientific_name

    class Meta:
        ordering = ['scientific_name']


class Register(BaseModel):
    """Register model."""

    id = models.AutoField(primary_key=True)
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    forest = models.ForeignKey(Forest,
                               on_delete=models.CASCADE)
    reference = models.ForeignKey(Reference,
                                  on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=10,
                                   decimal_places=7,
                                   null=True,
                                   blank=True)
    longitude = models.DecimalField(max_digits=10,
                                    decimal_places=7,
                                    null=True,
                                    blank=True)
    stage = EnumIntegerField(enum=StageType)
    state = EnumIntegerField(enum=StateType)

    def __str__(self):
        return '-'.join([str(self.id), self.species.name, self.forest.name])
