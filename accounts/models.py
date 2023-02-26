from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, date_of_birth, mobile, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        if not password:
            raise ValueError('Password is not provided')
        if User.objects.filter(mobile = mobile).exists():
            raise ValueError('Номер есть в базе')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            date_of_birth=date_of_birth,
            last_name=last_name,
            mobile=mobile,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name, date_of_birth, mobile, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, first_name, last_name, date_of_birth, mobile, **extra_fields)

    def create_superuser(self, email, password, first_name, last_name, date_of_birth, mobile, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, first_name, last_name, date_of_birth, mobile, **extra_fields)


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(db_index=True, unique=True, max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(blank=True)
    date_joined = models.DateTimeField(default=timezone.now)

    address = models.CharField(max_length=255, null=True)
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    mobile = models.CharField(validators=[phoneNumberRegex], max_length=16, unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth', 'mobile']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
