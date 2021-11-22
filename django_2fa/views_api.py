from django.contrib.auth.decorators import login_required
from django import http

from fido2 import cbor
from fido2.server import Fido2Server


@login_required
def register_begin(request):
  pass

@login_required
def register_complete(request):
  pass

@login_required
def authenticate_begin(request):
  pass

@login_required
def authenticate_complete(request):
  pass
