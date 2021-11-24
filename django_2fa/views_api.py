from django.conf import settings
from django.contrib.auth.decorators import login_required
from django import http
from django.views.decorators.csrf import csrf_exempt

from fido2 import cbor
from fido2.client import ClientData
from fido2.ctap2 import AttestationObject, AuthenticatorData
from fido2.server import Fido2Server
from fido2.webauthn import PublicKeyCredentialRpEntity

import django_2fa.settings as mfa_settings


def debug_verify_origin(*args, **kwargs):
  return True


def fido_server(request):
  host = request.get_host().split(":")[0]
  rp = PublicKeyCredentialRpEntity(host, mfa_settings.MFA_FIDO_KEY_NAME)

  if settings.DEBUG:
    return Fido2Server(rp, verify_origin=debug_verify_origin)

  return Fido2Server(rp)


@csrf_exempt
@login_required
def register_begin(request):
  data, state = fido_server(request).register_begin(
    {
      "id": bytes(f"{request.user.id}".encode()),
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
  data = cbor.decode(request.body)

  client_data = ClientData(data["clientDataJSON"])
  att_obj = AttestationObject(data["attestationObject"])

  print("CLIENT:", client_data)
  print("ATT:", att_obj)

  auth_data = fido_server(request).register_complete(request.session['fido-state'], client_data, att_obj)

  print("CRED DATA", auth_data.credential_data)

  del request.session['fido-state']

  return http.JsonResponse({'status': "OK"})

@csrf_exempt
@login_required
def authenticate_begin(request):
  pass

@csrf_exempt
@login_required
def authenticate_complete(request):
  pass
