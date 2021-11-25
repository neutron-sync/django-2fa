from django.urls import path

import django_2fa.views as mfa_views
import django_2fa.views_api as mfa_api_views
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

  path('fido/<str:device>/reg-begin/', mfa_api_views.register_begin, name='fido-reg-begin'),
  path('fido/<str:device>/reg-complete/', mfa_api_views.register_complete, name='fido-reg-complete'),
  path('fido/<str:device>/auth-begin/', mfa_api_views.authenticate_begin, name='fido-auth-begin'),
  path('fido/<str:device>/auth-complete/', mfa_api_views.authenticate_complete, name='fido-auth-complete'),
]
