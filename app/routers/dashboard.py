from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Member, Trainer, Membership, Payment, Attendance
from app.auth import require_roles

router=APIRouter(prefix="/dashboard",tags=["Dashboard"])

@router.get("/summary")
def summary(db:Session=Depends(get_db),_=Depends(require_roles("admin","trainer"))):
    today=date.today()
    active=db.query(Membership).filter(Membership.end_date>=today,Membership.status=="active").count()
    month_start=today.replace(day=1)
    next_month=(month_start.replace(day=28)+timedelta(days=4)).replace(day=1)
    paid_rows=db.query(Payment.amount).filter(Payment.status=="paid",Payment.payment_date>=month_start,Payment.payment_date<next_month).all()
    revenue=sum(float(row[0]) for row in paid_rows)
    attendance=db.query(Attendance).filter(Attendance.check_in>=datetime.combine(today,datetime.min.time())).count()
    pending=db.query(Payment).filter(Payment.status=="pending").count()
    return {"total_members":db.query(Member).count(),"active_memberships":active,"total_trainers":db.query(Trainer).count(),"today_attendance":attendance,"monthly_revenue":float(revenue or 0),"pending_payments":pending}
