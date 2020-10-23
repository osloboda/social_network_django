from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UniqueConstraint
    username = models.CharField(unique=True, max_length=10)
    email = None
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_request = models.DateTimeField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        ordering = ('date_joined',)
        db_table = 'users'

    def __str__(self):
        return self.username


class POST(models.Model):
    text = models.CharField(max_length=500)
    title = models.CharField(max_length=75)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class LIKE(models.Model):
    post = models.ForeignKey(POST, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_date = models.DateField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['post', 'author'],
                name='unique like'
            )
        ]
