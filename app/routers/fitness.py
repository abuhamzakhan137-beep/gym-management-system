from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import WorkoutPlan, DietPlan, Member, Trainer
from app.schemas import PlanAssignmentIn, PlanAssignmentOut
from app.auth import require_roles

router=APIRouter(tags=["Workout and Diet Plans"])

def create_plan(model,data,db):
    if not db.query(Member).get(data.member_id): raise HTTPException(404,"Member not found")
    if data.trainer_id and not db.query(Trainer).get(data.trainer_id): raise HTTPException(404,"Trainer not found")
    obj=model(**data.model_dump(exclude_none=True)); db.add(obj); db.commit(); db.refresh(obj); return obj

@router.post("/workouts/",response_model=PlanAssignmentOut)
def add_workout(data:PlanAssignmentIn,db:Session=Depends(get_db),_=Depends(require_roles("admin","trainer"))):
    return create_plan(WorkoutPlan,data,db)

@router.get("/workouts/",response_model=list[PlanAssignmentOut])
def workouts(db:Session=Depends(get_db),_=Depends(require_roles("admin","trainer","member"))):
    return db.query(WorkoutPlan).order_by(WorkoutPlan.id.desc()).all()

@router.post("/diet-plans/",response_model=PlanAssignmentOut)
def add_diet(data:PlanAssignmentIn,db:Session=Depends(get_db),_=Depends(require_roles("admin","trainer"))):
    return create_plan(DietPlan,data,db)

@router.get("/diet-plans/",response_model=list[PlanAssignmentOut])
def diets(db:Session=Depends(get_db),_=Depends(require_roles("admin","trainer","member"))):
    return db.query(DietPlan).order_by(DietPlan.id.desc()).all()
