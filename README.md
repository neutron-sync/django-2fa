# Django 2FA

two factor authentication support for Django

## Motivation

There are other good Django 2nd factor authentication libraries out there, however, the higher level libraries do not support e-mail and FIDO hardware keys as a second factor by default. Thus, django-2fa supports FIDO and E-Mail by default and additional authentication methods will be added upon request.

## Supported 2nd Factors

- HOTP via e-mail
- TOTP via authernicator apps
- FIDO via hardware tokens

## Installation

`pip install django-2fa`

## Configuration

You will need to configure django-2fa to use it in your Django project. Django-2fa works out of the box with minimal configuration, however, you will most likely want to do more configuration such as overriding the HTML templates or using the provided API so that it fits into the style of your project.

**See our [configuration docs](https://github.com/neutron-sync/django-2fa/blob/main/docs/config.md) for more detailed information on the process.**

## Additional Subjects

- [API Details](https://github.com/neutron-sync/django-2fa/blob/main/docs/api.md)
- [Protecting View with a 2nd Factor](https://github.com/neutron-sync/django-2fa/blob/main/docs/protecting-views.md)

## Shameless Plugs

I built this library originally for the [NeutronSync Service](https://www.neutronsync.com/). So if you would like to support this project please support the service with a subscription to NeutronSync or a [donation](https://github.com/sponsors/neutron-sync) to the open source libraries. Django 2FA is included by default in the Neutron Sync Server project.
