"""
routers/users.py  —  User profile & admin user management
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from core.security import get_current_user, get_current_admin, hash_password
from models.user   import User
from schemas       import UserOut, UserUpdate, UserCreate

router = APIRouter()


# ── Own profile ───────────────────────────────────────────────
@router.get("/me", response_model=UserOut, summary="Get my profile")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserOut, summary="Update my profile")
def update_me(
    payload:      UserUpdate,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    if payload.name:
        current_user.name = payload.name
    if payload.email:
        if db.query(User).filter(User.email == payload.email, User.id != current_user.id).first():
            raise HTTPException(status_code=400, detail="Email already taken")
        current_user.email = payload.email
    db.commit()
    db.refresh(current_user)
    return current_user


@router.delete("/me", summary="Delete my account")
def delete_me(
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    db.delete(current_user)
    db.commit()
    return {"message": "Account deleted successfully"}


# ── Admin: manage all users ───────────────────────────────────
@router.get("/", response_model=List[UserOut], summary="[Admin] List all users")
def list_users(
    skip:  int = 0,
    limit: int = 20,
    db:    Session = Depends(get_db),
    _:     User    = Depends(get_current_admin),
):
    return db.query(User).offset(skip).limit(limit).all()


@router.get("/{user_id}", response_model=UserOut, summary="[Admin] Get user by ID")
def get_user(
    user_id: int,
    db:      Session = Depends(get_db),
    _:       User    = Depends(get_current_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}/toggle-active",
              response_model=UserOut,
              summary="[Admin] Activate / deactivate user")
def toggle_active(
    user_id: int,
    db:      Session = Depends(get_db),
    _:       User    = Depends(get_current_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = not user.is_active
    db.commit()
    db.refresh(user)
    return user
