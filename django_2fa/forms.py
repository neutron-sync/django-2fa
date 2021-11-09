from django import forms

from django_2fa.models import Device


class MFAForm(forms.Form):
  mfa_code = forms.CharField()


class AddDeviceForm(forms.Form):
  name = forms.CharField(max_length=64, label="Device Name")
  device_type = forms.ChoiceField(choices=Device.DEVICE_TYPES)
  secret = forms.CharField(max_length=32, widget=forms.HiddenInput)
