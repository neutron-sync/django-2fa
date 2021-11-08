from django import forms

from django_2fa.models import Device


class MFAForm(forms.Form):
  mfa_code = forms.CharField()
