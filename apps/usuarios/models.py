from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.urls import reverse

class Usuario(AbstractUser):
    def __str__(self):
        return self.get_full_name()

    class Meta:
        ordering = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        self.username = self.email
        super(Usuario, self).save(*args, **kwargs)

