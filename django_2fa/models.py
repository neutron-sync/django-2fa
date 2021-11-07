from django.conf import settings
from django.db import models

from encrypted_fields.fields import EncryptedTextField


class Device(models.Model):
  DEVICE_TYPES = (
    ('email', 'E-Mail'),
    ('app', 'Authenicator App'),
    ('hkey', 'Hardware Key'),
  )

  name = models.CharField(max_length=64)
  device_type = models.CharField(max_length=10, choices=DEVICE_TYPES)
  secret = EncryptedTextField(blank=True, null=True)
  counter = models.PositiveIntegerField(default=0)

  owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

  created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name
