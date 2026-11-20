from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import RegisterIn, LoginIn, TokenOut, UserOut
from app.auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserOut)
def register(data: RegisterIn, db: Session = Depends(get_db)):
    if data.role not in ("admin", "trainer", "member"):
        raise HTTPException(400, "Role must be admin, trainer or member")
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(409, "Email is already registered")
    user = User(full_name=data.full_name, email=data.email, password_hash=hash_password(data.password), role=data.role)
    db.add(user); db.commit(); db.refresh(user)
    return user

@router.post("/login", response_model=TokenOut)
def login(data: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Incorrect email or password")
    if not user.is_active:
        raise HTTPException(403, "Account is inactive")
    return {"access_token": create_access_token(user), "user": user}

@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user
