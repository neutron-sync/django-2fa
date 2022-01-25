# API Details

You can use the API to implement a custom workflow for you 2 factor application. This document details endpoints available. Each endpoint is listed using the standard URL prefix `/2fa`.

## Common API

This set of endpoints are used to start the setup process and remove devices for all types. Additionally, for the email and app types, it used to complete the setup process.

### GET /2fa/devices/json

Get a list of available 2nd factor devices for the authenticated user.

**Query Parameters:**

*None*


**Example Reponse:**

```json
{
  "devices": [
    {
      "id": 4,
      "name": "EDog",
      "device_type": "email",
      "setup_complete": true,
      "created": "2021-12-23T16:21:59.976439+00:00"
    }
  ]
}
```

### POST /2fa/devices/add/json

First step in adding a 2nd factor device.

**Body Parameters: (All Required)**

- `name`: Device name, max length: 64 characters
- `device_type`: Device type, choices: email, app, hkey

**Example Response:**

```json
{
  "id": 4,
  "name": "EDog",
  "device_type": "email",
  "setup_complete": false,
  "created": "2021-12-23T16:21:59.976439+00:00"
}
```

### POST /2fa/devices/<device-id>/complete/json

Complete the process of adding a 2nd factor device for email and app types.

**Body Parameters: (All Required)**

- `mfa_code`: Code given by device.

**Example Response:**

```json
{
  "id": 4,
  "name": "EDog",
  "device_type": "email",
  "setup_complete": true,
  "created": "2021-12-23T16:21:59.976439+00:00"
}
```

### GET /2fa/devices/<device-id>/remove/json

Remove a 2nd factor device.

**Query Parameters:**

*None*

**Example Response:**

```json
{
  "status": "deleted"
}
```

## FIDO API

This set of endpoints are used to complete the FIDO setup process. The FIDO setup process is more invovled and currently relies on the key process being supported by the browser. Thus, many of the these endpoints have responses encoded in [CBOR encoding](https://cbor.io/) which is encoding scheme supported by FIDO keys. [cbor.js](https://github.com/neutron-sync/django-2fa/blob/main/django_2fa/static/2fa/cbor.js) is included to implement the workflow in Javascript.

  path('fido/<str:device>/reg-begin/', mfa_api_views.register_begin, name='fido-reg-begin'),
  path('fido/<str:device>/reg-complete/', mfa_api_views.register_complete, name='fido-reg-complete'),
  path('fido/<str:device>/auth-begin/', mfa_api_views.authenticate_begin, name='fido-auth-begin'),
  path('fido/<str:device>/auth-complete/', mfa_api_views.authenticate_complete, name='fido-auth-complete'),


path('request/<str:token>/', mfa_views.mfa_request, name='mfa-request'),
  path('request-complete/<str:token>/', mfa_views.mfa_request_complete, name='mfa-request-complete'),
  path('request-use/<str:token>/', mfa_api_views.request_use, name='mfa-request-use'),
