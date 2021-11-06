from django.contrib import admin

from django_2fa.models import Device


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
  list_display = ('name', 'owner', 'created')
  date_hierarchy = 'created'
  search_fields = ('name', 'owner__username')

  raw_id_fields = ('owner',)
