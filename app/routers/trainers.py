from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Trainer
from app.schemas import TrainerIn, TrainerOut
from app.auth import require_roles

router = APIRouter(prefix="/trainers", tags=["Trainers"])

@router.post("/", response_model=TrainerOut)
def create(data: TrainerIn, db: Session = Depends(get_db), _=Depends(require_roles("admin"))):
    if db.query(Trainer).filter(Trainer.email == data.email).first(): raise HTTPException(409, "Trainer email exists")
    obj=Trainer(**data.model_dump()); db.add(obj); db.commit(); db.refresh(obj); return obj

@router.get("/", response_model=list[TrainerOut])
def list_all(db: Session = Depends(get_db), _=Depends(require_roles("admin", "trainer"))):
    return db.query(Trainer).order_by(Trainer.id.desc()).all()

@router.put("/{item_id}", response_model=TrainerOut)
def update(item_id: int, data: TrainerIn, db: Session = Depends(get_db), _=Depends(require_roles("admin"))):
    obj=db.query(Trainer).get(item_id)
    if not obj: raise HTTPException(404, "Trainer not found")
    for k,v in data.model_dump().items(): setattr(obj,k,v)
    db.commit(); db.refresh(obj); return obj

@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db), _=Depends(require_roles("admin"))):
    obj=db.query(Trainer).get(item_id)
    if not obj: raise HTTPException(404, "Trainer not found")
    db.delete(obj); db.commit(); return {"message":"Trainer deleted"}
