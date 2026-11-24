from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='пользователь',
    )
    avatar = models.CharField(
        'аватар',
        max_length=255,
        default='img/avatar.png',
    )

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'

    def __str__(self):
        return self.user.username
