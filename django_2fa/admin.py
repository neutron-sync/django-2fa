from django.contrib import admin

from django_2fa.models import Device, MFARequest


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
  list_display = ('name', 'setup_complete', 'owner', 'created')
  list_filter = ('setup_complete',)
  date_hierarchy = 'created'
  search_fields = ('name', 'owner__username', 'owner__email', 'owner__first_name', 'owner__last_name')

  raw_id_fields = ('owner',)

  fields = ('name', 'device_type', 'counter', 'counter_expire', 'setup_complete', 'owner')


@admin.register(MFARequest)
class MFARequestAdmin(admin.ModelAdmin):
  list_display = ('slug', 'completed', 'used', 'owner', 'created')
  list_filter = ('completed', 'used')
  date_hierarchy = 'created'
  search_fields = ('slug',)
  raw_id_fields = ('owner',)
