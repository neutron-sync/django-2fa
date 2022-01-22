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

**See our [configuration docs]() for more detailed information on the process.**
