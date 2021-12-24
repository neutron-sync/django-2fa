import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone

import jwt
import pyotp
from encrypted_fields.fields import EncryptedTextField
from haikunator import Haikunator

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

  def to_dict(self):
    return {
      'id': self.id,
      'name': self.name,
      'device_type': self.device_type,
      'setup_complete': self.setup_complete,
      'setup_url': self.setup_url,
      'created': self.created.isoformat(),
    }

  def verify_code(self, code):
    if self.device_type == 'email':
      now = timezone.now()
      if self.counter_expire and now <= self.counter_expire:
        hotp = pyotp.HOTP(self.secret)
        return hotp.verify(code, self.counter)

    elif self.device_type == 'app':
      totp = pyotp.TOTP(self.secret)
      return totp.verify(code)

    return False

  @property
  def setup_url(self):
    if not self.setup_complete and self.device_type == 'app':
      return self.provision_url

  @property
  def provision_url(self):
    totp = pyotp.totp.TOTP(self.secret)
    return totp.provisioning_uri(name=f"User-{self.owner.id}", issuer_name=mfa_settings.MFA_ISSUER_NAME)

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


class MFARequest(models.Model):
  slug = models.SlugField(max_length=75)
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  completed = models.BooleanField(default=False)

  created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.slug


  @property
  def token(self):
    encoded_jwt = jwt.encode(
      {
        "slug": self.slug,
        "exp": timezone.now() + datetime.timedelta(minutes=mfa_settings.MFA_TOKEN_EXPIRE)
      },
      settings.SECRET_KEY,
      algorithm="HS256"
    )
    return encoded_jwt

  @classmethod
  def generate(cls, user):
    haikunator = Haikunator()

    while 1:
      slug = haikunator.haikunate(token_length=5)
      request = cls(slug=slug, owner=user)

      try:
        request.save()

      except:
        continue

      else:
        return request

  @classmethod
  def get_from_token(cls, token, owner=None):
    data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    if owner:
      return cls.objects.get(slug=data['slug'], completed=False, owner=owner)

    return cls.objects.get(slug=data['slug'], completed=False)
