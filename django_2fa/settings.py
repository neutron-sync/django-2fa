from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.translation import gettext as _


MFA_URL = getattr(settings, 'MFA_URL', '/2fa/login/')
MFA_REDIRECT_FIELD = getattr(settings, 'MFA_REDIRECT_FIELD', REDIRECT_FIELD_NAME)
MFA_EMAIL_SUBJECT = getattr(settings, 'MFA_EMAIL_SUBJECT', _('Temporary Authorization Code'))
MFA_ISSUER_NAME = getattr(settings, 'MFA_ISSUER_NAME', _('Django-2FA'))
