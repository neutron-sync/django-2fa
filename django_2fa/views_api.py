import base64

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django import http
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from fido2 import cbor
from fido2.client import ClientData
from fido2.ctap2 import AttestationObject, AuthenticatorData
from fido2.server import Fido2Server
from fido2.webauthn import PublicKeyCredentialRpEntity

from django_2fa.models import Device

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
def register_begin(request, device=None):
  device = get_object_or_404(Device, id=device, owner=request.user, setup_complete=False)
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
def register_complete(request, device=None):
  device = get_object_or_404(Device, id=device, owner=request.user, setup_complete=False)
  data = cbor.decode(request.body)

  client_data = ClientData(data["clientDataJSON"])
  att_obj = AttestationObject(data["attestationObject"])
  auth_data = fido_server(request).register_complete(request.session['fido-state'], client_data, att_obj)

  device.secret = base64.b64encode(auth_data.credential_data).decode()
  device.setup_complete = True
  device.save()

  del request.session['fido-state']

  return http.JsonResponse({'status': "OK"})


@csrf_exempt
@login_required
def authenticate_begin(request, device=None):
  pass


@csrf_exempt
@login_required
def authenticate_complete(request, device=None):
  pass
