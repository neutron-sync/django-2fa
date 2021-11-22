from django.contrib.auth.decorators import login_required
from django import http
from django.views.decorators.csrf import csrf_exempt

from fido2 import cbor
from fido2.server import Fido2Server
from fido2.webauthn import PublicKeyCredentialRpEntity

import django_2fa.settings as mfa_settings


def fido_server():
  rp = PublicKeyCredentialRpEntity(mfa_settings.MFA_FIDO_KEY_ID, mfa_settings.MFA_FIDO_KEY_NAME)
  return Fido2Server(rp)

@csrf_exempt
@login_required
def register_begin(request):
  data, state = fido_server().register_begin(
    {
      "id": request.user.id,
      "name": request.user.username,
      "displayName": request.user.username,
      "icon": mfa_settings.MFA_ICON
    },
    [],
    user_verification="discouraged",
    authenticator_attachment="cross-platform",
  )

  request.session['fido-state'] = state

  return http.HttpResponse(cbor.encode(data), content_type="application/cbor")

@csrf_exempt
@login_required
def register_complete(request):
  pass

@csrf_exempt
@login_required
def authenticate_begin(request):
  pass

@csrf_exempt
@login_required
def authenticate_complete(request):
  pass
