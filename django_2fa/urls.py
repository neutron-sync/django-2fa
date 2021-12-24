from django.urls import path

import django_2fa.views as mfa_views
import django_2fa.views_api as mfa_api_views
from django_2fa.apps import Django2FaConfig


app_name = Django2FaConfig.name

urlpatterns = [
  path('test/', mfa_views.test_2fa, name='test'),
  path('login/verify/<str:device>/', mfa_views.login_2fa_verify, name='verify'),
  path('login/', mfa_views.login_2fa, name='login'),

  path('request/<str:token>/', mfa_views.mfa_request, name='mfa-request'),
  path('request-complete/<str:token>/', mfa_views.mfa_request_complete, name='mfa-request-complete'),
  path('request-use/<str:token>/', mfa_api_views.request_use, name='mfa-request-use'),

  path('devices/', mfa_views.devices_list, name='devices'),
  path('devices/json', mfa_views.devices_list, name='devices-json', kwargs={'response_type': 'json'}),

  path('devices/add/', mfa_views.device_add, name='device-add'),
  path('devices/add/json', mfa_views.device_add_json, name='device-add-json'),

  path('devices/<str:device>/remove/', mfa_views.device_remove, name='device-remove'),
  path('devices/<str:device>/remove/json', mfa_views.device_remove, name='device-remove-json', kwargs={'response_type': 'json'}),

  path('devices/<str:device>/complete/', mfa_views.device_complete, name='device-complete'),
  path('devices/<str:device>/complete/json', mfa_views.device_complete_json, name='device-complete-json'),

  path('fido/<str:device>/reg-begin/', mfa_api_views.register_begin, name='fido-reg-begin'),
  path('fido/<str:device>/reg-complete/', mfa_api_views.register_complete, name='fido-reg-complete'),
  path('fido/<str:device>/auth-begin/', mfa_api_views.authenticate_begin, name='fido-auth-begin'),
  path('fido/<str:device>/auth-complete/', mfa_api_views.authenticate_complete, name='fido-auth-complete'),
]
