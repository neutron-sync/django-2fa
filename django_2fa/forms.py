from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from django_2fa.models import Device


class MFAForm(forms.Form):
  mfa_code = forms.CharField(label=_("Authorization Code"))

  def __init__(self, device, *args, **kwargs):
    self.device = device
    super().__init__(*args, **kwargs)

  def clean(self):
    cleaned_data = super().clean()
    if not self.device.verify_code(cleaned_data['mfa_code']):
      raise ValidationError(_("Authorization code does not match."))

    return cleaned_data


class AddDeviceForm(forms.ModelForm):
  class Meta:
    model = Device
    fields = ['name', 'device_type']

  def __init__(self, owner, *args, **kwargs):
    self.owner = owner
    super().__init__(*args, **kwargs)

  def clean_device_type(self):
    data = self.cleaned_data['device_type']
    if data == 'email':
      if not self.owner.email:
        raise ValidationError(_("An e-mail must be associated with this account."))

      if Device.objects.filter(device_type='email', owner=self.owner).count() > 1:
          raise ValidationError(_("Only one e-mail authenticator is allowed."))

    return data

  def clean(self):
    cleaned_data = super().clean()
    if Device.objects.filter(name=cleaned_data['name'], owner=self.owner).count() > 0:
      raise ValidationError(_("Device name is already used."))

    return cleaned_data

  def save(self):
    obj = super().save(commit=False)
    obj.owner = self.owner
    obj.save()
    return obj
