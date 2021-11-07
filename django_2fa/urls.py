from django.urls import path

import django_2fa.views as mfa_views
from django_2fa.apps import Django2FaConfig


app_name = Django2FaConfig.name

urlpatterns = [
  path('test/', mfa_views.test_2fa, name='test'),
  path('login/', mfa_views.login_2fa, name='login'),
]
