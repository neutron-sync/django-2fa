from django import forms

from django_2fa.models import Device


class MFAForm(forms.ModelForm):
  class Meta:
    model = Device
