from fastapi import APIRouter, Depends, HTTPException, status
from ..services.supabase_client import get_supabase_client
from ..schemas.user import UserCreate, UserLogin
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