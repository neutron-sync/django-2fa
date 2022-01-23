# Django 2FA Configuration

## Environmental Variables - *Required*

`SALT_KEY`: Set to a random string for encrypting secret database fields. 36 character string recommended.

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
| `MFA_URL` | `'/2fa/login/'` | 2nd login url, only change if you change the urlpattern above. |
| `MFA_REDIRECT_FIELD` | `next` | URL query parameter field used to redirect login. Default set to Django default parameter name. |
| `MFA_EMAIL_SUBJECT` | `'Temporary Authorization Code'` | Subject line for e-mail 2nd factor auth. |
| `MFA_ISSUER_NAME` | `'Django-2FA'` | Name of issuer shown in authenticator apps.  |
| `MFA_PROTECT_ALL_AUTHED` | `False` | When `True` if a user is logged in, then two factor auth will always be enforced. |
| `MFA_PROTECT_PATH_STARTSWITH` | `None` | List of URL paths that start with strings listed that will required 2 factor auth. For example: `['/admin/', '/account/']` |
| `MFA_PROTECT_PATH_EXACT` | `None` | List of exact URL paths that if matched will require 2 factor auth. |
| `MFA_ICON` | `"https://github.com/neutron-sync/django-2fa/raw/main/django_2fa/static/2fa/2fa-icon.png"` | Icon show in 2 factor auth apps. |
| `MFA_FIDO_KEY_NAME` | `f"{HOST} 2FA"` | Host name stored in FIDO key. |
| `MFA_TOKEN_EXPIRE` | `15` | Expiration in minutes for how long an e-mail token will last. |
