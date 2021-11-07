from django import http
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse

from django_2fa.decorators import mfa_login_required
from django_2fa.models import Device
import django_2fa.settings as mfa_settings

@mfa_login_required
def test_2fa(request):
  return http.HttpResponse('2FA Successful', content_type="text/plain")


@login_required
def login_2fa(request):
  devices = Device.objects.filter(owner=request.user).order_by('name')
  goto = request.GET.get(mfa_settings.MFA_REDIRECT_FIELD, settings.LOGIN_REDIRECT_URL)

  if devices.count() == 0:
    return http.HttpResponseRedirect(goto)

  return TemplateResponse(request, '2fa/login.html', {'devices': devices, 'goto': goto})


@login_required
def login_2fa_verify(request, device):
  form = MFAForm(request.POST or None)
  goto = request.get.GET(mfa_settings.MFA_REDIRECT_FIELD, settings.LOGIN_REDIRECT_URL)

  if request.method == 'POST':
    if form.is_valid(request.user):
      goto = request.POST.get(mfa_settings.MFA_REDIRECT_FIELD, goto)
      return http.HttpResponseRedirect(goto)

  return TemplateResponse(request, '2fa/verify.html', {'form': form, 'goto': goto})
