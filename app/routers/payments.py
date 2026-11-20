from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Payment, Member
from app.schemas import PaymentIn, PaymentOut
from app.auth import require_roles

router=APIRouter(prefix="/payments",tags=["Payments"])

@router.post("/",response_model=PaymentOut)
def create(data: PaymentIn,db:Session=Depends(get_db),_=Depends(require_roles("admin"))):
    if data.amount < 0: raise HTTPException(400,"Amount cannot be negative")
    if not db.query(Member).get(data.member_id): raise HTTPException(404,"Member not found")
    obj=Payment(**data.model_dump(exclude_none=True)); db.add(obj); db.commit(); db.refresh(obj); return obj

@router.get("/",response_model=list[PaymentOut])
def list_all(db:Session=Depends(get_db),_=Depends(require_roles("admin"))):
    return db.query(Payment).order_by(Payment.payment_date.desc()).all()
