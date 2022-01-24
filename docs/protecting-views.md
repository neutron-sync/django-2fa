# Protecting View with a 2nd Factor

When a user is authenticated and a second factor has been verified, the key `'2fa_verfied'` contains the value of `True` on the session. Many views you will want to protect with a second factor. This document outlines the ways you can protect views to enforce a second factor.

**Note:** a user will bypass second factor checks if they do not have a second factor device available and the setup process is complete.

## 2FA Enforcement via View Decorator

To protect a single view, use the `mfa_login_required` decorator.

Example:

```python
from django_2fa.decorators import mfa_login_required

@mfa_login_required
def some_view(request):
  return blah_response()
```

## 2FA Enforcement via Settings

### MFA_PROTECT_ALL_AUTHED

When set to `True` this will enforce 2FA anytime a user is logged in. Be careful with this one, you probably don't want to use this one but it's there if you like foot guns.

### MFA_PROTECT_PATH_STARTSWITH

A list of URL paths that start with a particular prefix or prefixes. For these matches, 2FA will be enforced.

Example: `['/admin/', '/account/']`

### MFA_PROTECT_PATH_EXACT

A list of exact URL paths that when matched exactly, 2FA will be enforced.

Example: `['/account/change-password/', '/account/buy-expensive-stuff/']`

## Ensuring Everyone Always Has a Second Factor

Right now this isn't built into the library, however, if you enforce all users always having an e-mail address, then you can automatically add an e-mail authentication device for them. Note, you will want to make sure their e-mail is also verified and working.
