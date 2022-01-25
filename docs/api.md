# API Details

You can use the API to implement a custom workflow for your 2 factor application. This document details endpoints available. Each endpoint is listed using the standard URL prefix `/2fa`. Additionally, all endpoints require a user to authenticated.

## Common API

This set of endpoints are used to start the setup process and remove devices for all types. Additionally, for the email and app types, it used to complete the setup process.

### GET /2fa/devices/json

Get a list of available 2nd factor devices for the authenticated user.

**Query Parameters:** *None*

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

**Query Parameters:** *None*

**Example Response:**

```json
{
  "status": "deleted"
}
```

## FIDO API

This set of endpoints are used to complete the FIDO setup process. The FIDO setup process is more invovled and currently relies on the key process being supported by the browser. Thus, many of the these endpoints have responses encoded in [CBOR encoding](https://cbor.io/) which is encoding scheme supported by FIDO keys. [cbor.js](https://github.com/neutron-sync/django-2fa/blob/main/django_2fa/static/2fa/cbor.js) is included to implement the workflow in Javascript. When implementing your own FIDO process you may want to reference the Javascript for [completion](https://github.com/neutron-sync/django-2fa/blob/main/django_2fa/templates/2fa/complete-fido.html#L16-L38) and [verification](https://github.com/neutron-sync/django-2fa/blob/main/django_2fa/templates/2fa/verify-fido.html#L16-L40) that comes with Django 2FA.

### GET /2fa/fido/<device-id>/reg-begin/

**Query Parameters:** *None*

**Example Response: (CBOR Encoded)**

```python
{
  "publicKey": {
    "rp": {"id": "localhost", "name": "localhost 2FA"},
    "user": {
      "id": '31',
      "icon": "https://github.com/neutron-sync/django-2fa/raw/main/django_2fa/static/2fa/2fa-icon.png",
      "name": "paul",
      "displayName": "paul"
    },
    "challenge": 'BLAH44C9E0F0455CD7EBLAHFDAB72BLAHF82BLAHF6BLAHC0A90CFAC16975BLAH',
    "pubKeyCredParams": [
      {"alg": -7, "type": "public-key"},
      {"alg": -8, "type": "public-key"},
      {"alg": -37, "type": "public-key"},
      {"alg": -257, "type": "public-key"}
    ],
    "excludeCredentials": [],
    "authenticatorSelection": {
      "userVerification": "discouraged",
      "authenticatorAttachment": "cross-platform"
    }
  }
}
```

## POST /2fa/fido/<device-id>/reg-complete/

**Body Parameters: (CBOR Encoded)**

```javascript
{
  "attestationObject": new Uint8Array(attestation.response.attestationObject),
  "clientDataJSON": new Uint8Array(attestation.response.clientDataJSON)
}
```

**Example Response:**

```json
{"status": "OK"}
```

## GET /2fa/fido/<device-id>/auth-begin/

**Query Parameters:** *None*

**Example Response: (CBOR Encoded)**

```python
{
  "publicKey": {
    "rpId": "localhost",
    "challenge": 'BLAH71946BLAH55ABLAH5232BLAHDEA1BLAH1AC46BLAH8FC7CBLAH32C336BLAH',
    "allowCredentials": [
      {
        "id": 'BLAHD2589BAB63A66ACBLAHFDCE0BLAHB8783D1DBLAH8AC3CBLAHCC00AA4BLAH05927B9D3DC968BLAH8262BLAH3617E8921BLAHD7B85BLAHD61DBLAH468BLAH2',
        "type": "public-key"
      }
    ]
  }
}
```

## POST /2fa/fido/<device-id>/auth-complete/

**Body Parameters: (CBOR Encoded)**

```javascript
{
  "credentialId": new Uint8Array(assertion.rawId),
  "authenticatorData": new Uint8Array(assertion.response.authenticatorData),
  "clientDataJSON": new Uint8Array(assertion.response.clientDataJSON),
  "signature": new Uint8Array(assertion.response.signature)
}
```

**Example Response:**

```json
{"status": "OK"}
```

## External App 2 Factor Auth

Request 2nd factor process completetion. See [external apps](external-apps.md) for more information about using 2nd factor auth with external applications.

### GET /2fa/request-use/<token>/

**Query Parameters:** *None*

**Example Response:**

```json
{"status": "OK"}
```
