from appservicecore.api_service import app
from fastapi import Response
from authservice.api.users import SignUp, SignIn
from authservice.models.auth_request_models import UserSignIn, UserSignUp


@app.get("/auth")
async def auth_main():
    return {"message": "Authservice running on port 7171"}


@app.post("/auth/account-signup")
async def signup_user(data: UserSignUp, response: Response):
    sign_up = SignUp(user=data)
    if sign_up.exists:
        response.status_code = 401
        return {'Message': 'User already registered'}
    sign_up.write()
    response.status_code = 200
    return {'Message': 'User successfully registered'}


@app.post("/auth/account-signin")
async def signin_user(data: UserSignIn, response: Response):
    sign_in = SignIn(user=data)
    if not sign_in.exists:
        response.status_code = 402
        return {'Message': 'User does not exist'}
    if sign_in.authenticated:
        response.status_code = 200
        return {'Message': 'Authentication successfull!'}
    else:
        response.status_code = 403
        return {'Message': 'Wrong password or email entered.'}
