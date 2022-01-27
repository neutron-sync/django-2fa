# 2 Factor Auth with External Apps

If you are building an external application that uses your Django app as an API, often times you want to use your 2nd factor login for the external application without having to re-implement all the coding needed to handle the 2nd factor. Additionally, with FIDO keys, sometimes the external application can not access the 2nd factor. For both these use cases, Django 2FA includes views and endpoints to faciliate an external application to authenticate with 2nd factors.

## Step 1 [External App]: Login and Obtain MFA Token URL

The external app should login the user with the `/2fa/login/external/json` endpoint. This endpoint will authenicate the user and start their session. Lastly, the endpoint will return the MFA URL if it is required for that user.

## Step 2 [User in Browser]: User Visits Token URL

The user will take the URL given in step one and open it in a browser of their choice. This URL takes them to `/2fa/request/<token>/`. If the token is valid, then the user is redirected to `/2fa/request-complete/<token>/` where they will be required to login with thier 2nd factor.

## Step 3 [External App]: Application Completes Process

The external application must wait for the login to complete. To verify the completetion, the application should check the endpoint `/2fa/request-use/<token>/`. This endpoint can be called multiple times. It will return a status code of 200 and JSON status of `OK` once the login is completed. In turn the session used by the external application will be updated as 2FA verified.
