from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.translation import gettext as _


MFA_URL = getattr(settings, 'MFA_URL', '/2fa/login/')
MFA_REDIRECT_FIELD = getattr(settings, 'MFA_REDIRECT_FIELD', REDIRECT_FIELD_NAME)
MFA_EMAIL_SUBJECT = getattr(settings, 'MFA_EMAIL_SUBJECT', _('Temporary Authorization Code'))
MFA_ISSUER_NAME = getattr(settings, 'MFA_ISSUER_NAME', _('Django-2FA'))

MFA_PROTECT_ALL_AUTHED = getattr(settings, 'MFA_PROTECT_ALL_AUTHED', False)
MFA_PROTECT_PATH_STARTSWITH = getattr(settings, 'MFA_PROTECT_PATH_STARTSWITH', None)
MFA_PROTECT_PATH_EXACT = getattr(settings, 'MFA_PROTECT_PATH_EXACT', None)

MFA_ICON = getattr(settings, 'MFA_ICON', "https://github.com/neutron-sync/django-2fa/raw/main/django_2fa/static/2fa/2fa-icon.png")

if settings.ALLOWED_HOSTS:
  HOST = settings.ALLOWED_HOSTS[0]

else:
  HOST = "localhost"

MFA_FIDO_KEY_NAME = getattr(settings, 'MFA_FIDO_KEY_NAME', f"{HOST} 2FA")
