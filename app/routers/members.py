from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Member
from app.schemas import MemberIn, MemberOut
from app.auth import require_roles

router = APIRouter(prefix="/members", tags=["Members"])

@router.post("/", response_model=MemberOut)
def create_member(data: MemberIn, db: Session = Depends(get_db), _=Depends(require_roles("admin", "trainer"))):
    if db.query(Member).filter(Member.email == data.email).first():
        raise HTTPException(409, "Member email already exists")
    obj = Member(**data.model_dump(exclude_none=True)); db.add(obj); db.commit(); db.refresh(obj); return obj

@router.get("/", response_model=list[MemberOut])
def list_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _=Depends(require_roles("admin", "trainer"))):
    return db.query(Member).order_by(Member.id.desc()).offset(skip).limit(min(limit, 200)).all()

@router.get("/{member_id}", response_model=MemberOut)
def get_member(member_id: int, db: Session = Depends(get_db), _=Depends(require_roles("admin", "trainer"))):
    obj = db.query(Member).get(member_id)
    if not obj: raise HTTPException(404, "Member not found")
    return obj

@router.put("/{member_id}", response_model=MemberOut)
def update_member(member_id: int, data: MemberIn, db: Session = Depends(get_db), _=Depends(require_roles("admin", "trainer"))):
    obj = db.query(Member).get(member_id)
    if not obj: raise HTTPException(404, "Member not found")
    for key, value in data.model_dump(exclude_none=True).items(): setattr(obj, key, value)
    db.commit(); db.refresh(obj); return obj

@router.delete("/{member_id}")
def delete_member(member_id: int, db: Session = Depends(get_db), _=Depends(require_roles("admin"))):
    obj = db.query(Member).get(member_id)
    if not obj: raise HTTPException(404, "Member not found")
    db.delete(obj); db.commit(); return {"message": "Member deleted"}
