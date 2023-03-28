from django.utils import timezone
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class HealthService(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    url = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        '''Create and save a user with the given email, and
        password.
        '''
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must have is_staff=True.'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must have is_superuser=True.'
            )

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):

    class Meta:
        permissions = (("change_author", "Can modify the author assigned to Reviews and Comments"),)
        verbose_name = "User"

    email = models.EmailField(
        unique=True,
        max_length=255,
        blank=False,
    )

    # All these field declarations are copied as-is
    # from `AbstractUser`
    first_name = models.CharField(
        'first name',
        max_length=30,
        blank=True,
    )
    last_name = models.CharField(
        'last name',
        max_length=150,
        blank=True,
    )
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text=(
            'Designates whether the user can log into '
            'this admin site.'
        ),
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text=(
            'Designates whether this user should be '
            'treated as active. Unselect this instead '
            'of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(
        'date joined',
        default=timezone.now,
    )

    anonymous_author = models.BooleanField(default=False)
    health_services = models.ManyToManyField(
        HealthService,
        related_name='health_services',
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


