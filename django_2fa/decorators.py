from functools import wraps
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import resolve_url

import django_2fa.settings as mfa_settings


def request_passes_test(auth_test_func, mfa_test_func, login_url=None, mfa_url=None, redirect_field_name=mfa_settings.MFA_REDIRECT_FIELD):
  def decorator(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
      path = request.build_absolute_uri()

      if auth_test_func(request.user):
        if mfa_test_func(request):
          return view_func(request, *args, **kwargs)

        else:
          resolved_login_url = resolve_url(mfa_url or mfa_settings.MFA_URL)

      else:
        resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)

      login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
      current_scheme, current_netloc = urlparse(path)[:2]
      if ((not login_scheme or login_scheme == current_scheme) and (not login_netloc or login_netloc == current_netloc)):
        path = request.get_full_path()

      return redirect_to_login(path, resolved_login_url, redirect_field_name)

    return _wrapped_view

  return decorator


def is_mfa_authed(request):
  user_id = request.session.get('2fa_verfied')
  if user_id and request.user.id:
    return True

  return False


def is_authed(user):
  return user.is_authenticated


def mfa_login_required(function=None, redirect_field_name=mfa_settings.MFA_REDIRECT_FIELD, login_url=None, mfa_url=None):
  actual_decorator = request_passes_test(
    is_authed,
    is_mfa_authed,
    login_url=login_url,
    mfa_url=mfa_url,
    redirect_field_name=redirect_field_name
  )

  if function:
    return actual_decorator(function)

  return actual_decorator
