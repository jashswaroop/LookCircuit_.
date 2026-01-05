from fastapi import APIRouter, Depends
from app.api import deps
from app.schemas.user import User

router = APIRouter()

@router.get("/me", response_model=User)
def read_user_me(
    current_user: User = Depends(deps.get_current_user),
):
    """
    Get current user.
    """
    return current_user

@router.put("/me", response_model=User)
def update_user_me(
    current_user: User = Depends(deps.get_current_user),
):
    """
    Update current user profile.
    TODO: Implement update logic with DB
    """
    return current_user
