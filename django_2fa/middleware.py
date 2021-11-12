from django import http

import django_2fa.settings as mfa_settings


class MFAProctectMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    needs_mfa = False

    if mfa_settings.MFA_PROTECT_PATH_STARTSWITH and request.path.startswith(mfa_settings.MFA_PROTECT_PATH_STARTSWITH):
      needs_mfa = True

    elif mfa_settings.MFA_PROTECT_PATH_EXACT and request.path in mfa_settings.MFA_PROTECT_PATH_EXACT:
      needs_mfa = True

    if needs_mfa and request.user.is_authenticated:
      user_id = request.session.get('2fa_verfied')
      if user_id and request.user.id:
        return self.get_response(request)

      q = http.QueryDict(mutable=True)
      q.update({mfa_settings.MFA_REDIRECT_FIELD: request.get_full_path()})
      goto = mfa_settings.MFA_URL + '?' + q.urlencode()
      return http.HttpResponseRedirect(goto)

    return self.get_response(request)
