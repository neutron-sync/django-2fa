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

Add `'django_2fa.middleware.MFAProctectMiddleware'` to your list of middleware after session and authentication middleware.

```python
MIDDLEWARE = [
  ...
  'django_2fa.middleware.MFAProctectMiddleware',
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

## Template Customization - *Optional*

Django 2FA comes with a set of views and templates out of the box that handle second factor authentication. The templates are based on [Materialize](https://materializecss.com/); however, they probably do not match your site style. The easiest way to customize the templates is to copy the templates to a Django app that comes before `django_2fa` in your `INSTALLED_APPS` list. Then you can customize the CSS colors or go further and customize the whole look and feel.

You will want to copy all the templates listed in `django_2fa/templates/2fa/`. See [Github](https://github.com/neutron-sync/django-2fa/tree/main/django_2fa/templates/2fa) to view and download all the templates. Below is a description of what each template is used for.

| Template | Description |
| -------- | ----------- |
| `add-device.html` | Initial form for adding a 2 factor device. |
| `base.html` | Base template for 2fa app templates. |
| `complete-fido.html` | second form used to complete the FIDO hardware device addition process. |
| `devices.html` | List of a users personal 2FA devices. |
| `email-code.html` | HTML e-mail sent with e-mail 2 factor requests. |
| `email-code.txt` | Plain text e-mail sent with e-mail 2 factor requests. |
| `login.html` | Initial page shown for 2 factor protected views. Lets the user choose with device to use for their second factor. |
| `request-completed.html` | When verifying a user for external applications like for a CLI application, this is the final success page. |
| `verify-fido.html` | Page for verifying FIDO devices. |
| `verify.html` | Page for verifying e-mail and authenticator app. Also used as the second form in the device addition process. |

## Custom Workflow Using the API

You can also build a complete customized workflow using the included API. See the [API Docs](api.md) for more information about using the API.

## Getting started

To get started you should take a look at the `2fa/devices/` endpoint. You will see a page with a list of all devices and the button to add a new device. From there you can follow the auth flow and make adjustments to the templates as needed.
