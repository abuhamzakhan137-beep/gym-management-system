from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import MembershipPlan, Membership, Member, Trainer
from app.schemas import PlanIn, PlanOut, MembershipIn, MembershipOut
from app.auth import require_roles

router = APIRouter(tags=["Memberships"])

@router.post("/plans/", response_model=PlanOut)
def create_plan(data: PlanIn, db: Session=Depends(get_db), _=Depends(require_roles("admin"))):
    if data.duration_days < 1 or data.price < 0: raise HTTPException(400,"Duration must be positive and price cannot be negative")
    obj=MembershipPlan(**data.model_dump()); db.add(obj); db.commit(); db.refresh(obj); return obj

@router.get("/plans/", response_model=list[PlanOut])
def list_plans(db: Session=Depends(get_db), _=Depends(require_roles("admin","trainer","member"))):
    return db.query(MembershipPlan).all()

@router.post("/memberships/", response_model=MembershipOut)
def create_membership(data: MembershipIn, db: Session=Depends(get_db), _=Depends(require_roles("admin"))):
    member=db.query(Member).get(data.member_id); plan=db.query(MembershipPlan).get(data.plan_id)
    if not member or not plan: raise HTTPException(404,"Member or membership plan not found")
    if data.trainer_id and not db.query(Trainer).get(data.trainer_id): raise HTTPException(404,"Trainer not found")
    start=data.start_date or date.today()
    obj=Membership(member_id=data.member_id,plan_id=data.plan_id,trainer_id=data.trainer_id,start_date=start,end_date=start+timedelta(days=plan.duration_days),status="active")
    db.add(obj); db.commit(); db.refresh(obj); return obj

@router.get("/memberships/", response_model=list[MembershipOut])
def list_memberships(db: Session=Depends(get_db), _=Depends(require_roles("admin","trainer"))):
    items=db.query(Membership).all()
    for x in items:
        if x.end_date < date.today(): x.status="expired"
    db.commit()
    return items
