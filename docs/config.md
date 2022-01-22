# Django 2FA Configuration

## settings.py - *Required*

Add `django_2fa` to your installed apps.

```python
INSTALLED_APPS = [
  ...
  'django_2fa',
]
```

## urls.py - *Required*

Add django_2fa URLs

```python
from django.urls import path, include

import django_2fa.urls

urlpatterns = [
  ...
  path('2fa/', include(django_2fa.urls)),
]
```

## settings.py - *Optional*

| Setting Name | Default | Description |
| ------------ | ------- | ----------- |
| `LOGIN_URL`  | `'/admin/login/'` | Standard Django setting. You probably want to change it to your custom login url |
| `LOGIN_REDIRECT_URL` | `'/'` | Standard Django setting. You probably want to change it to your custom post login url |

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

MFA_TOKEN_EXPIRE = getattr(settings, 'MFA_TOKEN_EXPIRE', 15)
