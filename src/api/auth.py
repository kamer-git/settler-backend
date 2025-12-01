from fastapi import APIRouter, Depends, HTTPException, status, Request
from ..services.supabase_client import get_supabase_client
from ..schemas.user import UserCreate, UserLogin, PasswordResetRequest, PasswordUpdateRequest
from gotrue.errors import AuthApiError
from supabase import Client

router = APIRouter()

@router.post("/signup")
def signup(user: UserCreate, supabase: Client = Depends(get_supabase_client)):
    """
    Handles user sign-up. For a smoother development experience, it's recommended
    to disable "Confirm email" in your Supabase project's authentication settings.
    This allows new users to be logged in immediately after signing up.
    """
    try:
        res = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
        })

        # If sign up is successful and a session is returned (i.e. email confirmation is off)
        # return the access token.
        if res.session:
            return {"access_token": res.session.access_token, "token_type": "bearer"}

        # If email confirmation is required, Supabase creates the user but doesn't return a session.
        # We must explicitly handle this case.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email confirmation is required. Please disable it in your Supabase settings for this flow to work."
        )

    except AuthApiError as e:
        # This will catch errors like "User already registered"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )

@router.post("/login")
def login(user: UserLogin, supabase: Client = Depends(get_supabase_client)):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
        return {"access_token": res.session.access_token, "token_type": "bearer"}
    except AuthApiError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message or "Invalid credentials"
        )

@router.post("/request-password-reset")
def request_password_reset(req: PasswordResetRequest, supabase: Client = Depends(get_supabase_client)):
    try:
        supabase.auth.reset_password_for_email(email=req.email)
        return {"message": "Password reset email sent."}
    except AuthApiError as e:
        # Avoid leaking information about whether an email exists
        return {"message": "If an account with this email exists, a password reset email has been sent."}


@router.post("/update-password")
def update_password(req: PasswordUpdateRequest, supabase: Client = Depends(get_supabase_client)):
    try:
        # Supabase uses the token from the password reset email to authenticate the user for this single action.
        user_response = supabase.auth.update_user(
            {"password": req.password}, 
            jwt=req.token
        )
        return {"message": "Password updated successfully."}
    except AuthApiError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)


@router.get("/verify")
def verify(token: str, supabase: Client = Depends(get_supabase_client)):
    try:
        user_response = supabase.auth.get_user(token)
        return user_response
    except AuthApiError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {e.message}"
        )