from django.urls import path

import django_2fa.views as mfa_views
from django_2fa.apps import Django2FaConfig


app_name = Django2FaConfig.name

urlpatterns = [
  path('test/', mfa_views.test_2fa, name='test'),
  path('login/verify/<str:device>/', mfa_views.login_2fa_verify, name='verify'),
  path('login/', mfa_views.login_2fa, name='login'),
  path('devices/', mfa_views.devices_list, name='devices'),
  path('devices/add/', mfa_views.device_add, name='device-add'),
  path('devices/<str:device>/remove/', mfa_views.device_remove, name='device-remove'),
  path('devices/<str:device>/complete/', mfa_views.device_complete, name='device-complete'),
]
