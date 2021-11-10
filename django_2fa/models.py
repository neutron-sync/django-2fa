import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone

import pyotp
from encrypted_fields.fields import EncryptedTextField

import django_2fa.settings as mfa_settings


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
  counter_expire = models.DateTimeField(blank=True, null=True)
  setup_complete = models.BooleanField(default=False)

  owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = [['name', 'owner']]

  def __str__(self):
    return self.name

  def verify_code(self, code):
    if self.device_type == 'email':
      now = timezone.now()
      if self.counter_expire and now <= self.counter_expire:
        hotp = pyotp.HOTP(self.secret)
        return hotp.verify(code, self.counter)

    return False

  def send_code(self):
    self.counter += 1
    self.counter_expire = timezone.now() + datetime.timedelta(minutes=15)
    self.save()

    hotp = pyotp.HOTP(self.secret)
    code = hotp.at(self.counter)

    context = {'device': self, 'code': code}
    txt_message = render_to_string('2fa/email-code.txt', context)
    html_message = render_to_string('2fa/email-code.html', context)

    send_mail(
      mfa_settings.MFA_EMAIL_SUBJECT,
      txt_message,
      settings.DEFAULT_FROM_EMAIL,
      [self.owner.email],
      html_message=html_message,
      fail_silently=False,
    )
