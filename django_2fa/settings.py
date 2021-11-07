from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME

MFA_URL = getattr(settings, 'MFA_URL', '/2fa/login/')
MFA_REDIRECT_FIELD = getattr(settings, 'MFA_REDIRECT_FIELD', REDIRECT_FIELD_NAME)
