from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Attendance, Member
from app.schemas import AttendanceIn, AttendanceOut
from app.auth import require_roles

router=APIRouter(prefix="/attendance",tags=["Attendance"])

@router.post("/check-in",response_model=AttendanceOut)
def check_in(data:AttendanceIn,db:Session=Depends(get_db),_=Depends(require_roles("admin","trainer"))):
    if not db.query(Member).get(data.member_id): raise HTTPException(404,"Member not found")
    open_record=db.query(Attendance).filter(Attendance.member_id==data.member_id,Attendance.check_out==None).first()
    if open_record: raise HTTPException(409,"Member is already checked in")
    obj=Attendance(member_id=data.member_id,notes=data.notes); db.add(obj); db.commit(); db.refresh(obj); return obj

@router.post("/{attendance_id}/check-out",response_model=AttendanceOut)
def check_out(attendance_id:int,db:Session=Depends(get_db),_=Depends(require_roles("admin","trainer"))):
    obj=db.query(Attendance).get(attendance_id)
    if not obj: raise HTTPException(404,"Attendance record not found")
    if obj.check_out: raise HTTPException(409,"Already checked out")
    obj.check_out=datetime.utcnow(); db.commit(); db.refresh(obj); return obj

@router.get("/",response_model=list[AttendanceOut])
def list_all(day:date|None=None,db:Session=Depends(get_db),_=Depends(require_roles("admin","trainer"))):
    q=db.query(Attendance)
    if day: q=q.filter(Attendance.check_in>=datetime.combine(day,datetime.min.time()),Attendance.check_in<datetime.combine(day,datetime.max.time()))
    return q.order_by(Attendance.check_in.desc()).limit(500).all()
