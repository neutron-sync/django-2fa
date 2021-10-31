from django.db import models
from encrypted_fields.fields import EncryptedCharField


class Device(models.Model):
  name = models.CharField(max_length=64)
  secret = EncryptedCharField(max_length=)
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name
