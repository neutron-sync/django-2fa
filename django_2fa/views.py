from django import http
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse

import pyotp

from django_2fa.decorators import mfa_login_required
from django_2fa.forms import MFAForm, AddDeviceForm
from django_2fa.models import Device
import django_2fa.settings as mfa_settings


@mfa_login_required
def test_2fa(request):
  return http.HttpResponse('2FA Successful', content_type="text/plain")


@login_required
def login_2fa(request):
  devices = Device.objects.filter(owner=request.user).order_by('name')

  if devices.count() == 0:
    goto = request.GET.get(mfa_settings.MFA_REDIRECT_FIELD, settings.LOGIN_REDIRECT_URL)
    return http.HttpResponseRedirect(goto)

  if devices.count() == 1:
    goto = reverse('django_2fa:verify', args=(str(devices[0].id),))
    return http.HttpResponseRedirect(goto)

  return TemplateResponse(request, '2fa/login.html', {'devices': devices, 'goto': goto})


@login_required
def login_2fa_verify(request, device=None):
  device = get_object_or_404(Device, id=device, owner=request.user)
  form = MFAForm(request.POST or None)
  goto = request.GET.get(mfa_settings.MFA_REDIRECT_FIELD, settings.LOGIN_REDIRECT_URL)

  if request.method == 'POST':
    if form.is_valid(request.user):
      goto = request.POST.get(mfa_settings.MFA_REDIRECT_FIELD, goto)
      return http.HttpResponseRedirect(goto)

  return TemplateResponse(request, '2fa/verify.html', {'form': form, 'goto': goto})


@login_required
def devices_list(request):
  devices = Device.objects.filter(owner=request.user).order_by('name')
  return TemplateResponse(request, '2fa/devices.html', {'devices': devices})


@login_required
def device_add(request):

  if request.method == 'GET':
    form = AddDeviceForm(None, initial={'secret': pyotp.random_base32()})

  if request.method == 'POST':
    form = AddDeviceForm(request.POST)
    if form.is_valid():
      return http.HttpResponseRedirect("../")

  return TemplateResponse(request, '2fa/add-device.html', {'form': form})


@login_required
def device_remove(request, device=None):
  pass
