from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from supabase import Client
from pydantic import ValidationError
from app.db.session import get_supabase
from app.schemas.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # This URL might need adjustment for Supabase flow

def get_current_user(
    token: str = Depends(oauth2_scheme),
    supabase: Client = Depends(get_supabase)
) -> User:
    try:
        # Verify the token with Supabase
        user_response = supabase.auth.get_user(token)
        
        if not user_response or not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        user_data = user_response.user
        
        # Map Supabase user to our internal schema
        # Note: metadata handling might be needed for profile fields
        return User(
            id=user_data.id,
            email=user_data.email,
            is_active=True # Default to true for authenticated users
        )
        
    except Exception as e:
        # Catch supabase errors or validation errors
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
