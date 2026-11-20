from datetime import datetime, date
from sqlalchemy import String, Integer, Float, Boolean, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(180), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), default="member")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Member(Base):
    __tablename__ = "members"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(180), unique=True, index=True)
    phone: Mapped[str] = mapped_column(String(30), default="")
    age: Mapped[int] = mapped_column(Integer, default=18)
    gender: Mapped[str] = mapped_column(String(30), default="Prefer not to say")
    joined_on: Mapped[date] = mapped_column(Date, default=date.today)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    notes: Mapped[str] = mapped_column(Text, default="")
    memberships = relationship("Membership", back_populates="member", cascade="all, delete-orphan")

class Trainer(Base):
    __tablename__ = "trainers"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(180), unique=True, index=True)
    phone: Mapped[str] = mapped_column(String(30), default="")
    specialization: Mapped[str] = mapped_column(String(120), default="General Fitness")
    experience_years: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

class MembershipPlan(Base):
    __tablename__ = "membership_plans"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)
    duration_days: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(Text, default="")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

class Membership(Base):
    __tablename__ = "memberships"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    plan_id: Mapped[int] = mapped_column(ForeignKey("membership_plans.id"))
    trainer_id: Mapped[int | None] = mapped_column(ForeignKey("trainers.id"), nullable=True)
    start_date: Mapped[date] = mapped_column(Date, default=date.today)
    end_date: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(20), default="active")
    member = relationship("Member", back_populates="memberships")
    plan = relationship("MembershipPlan")
    trainer = relationship("Trainer")

class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    membership_id: Mapped[int | None] = mapped_column(ForeignKey("memberships.id"), nullable=True)
    amount: Mapped[float] = mapped_column(Float)
    payment_date: Mapped[date] = mapped_column(Date, default=date.today)
    method: Mapped[str] = mapped_column(String(30), default="Cash")
    status: Mapped[str] = mapped_column(String(20), default="paid")
    reference: Mapped[str] = mapped_column(String(100), default="")
    member = relationship("Member")

class Attendance(Base):
    __tablename__ = "attendance"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    check_in: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    check_out: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    notes: Mapped[str] = mapped_column(String(255), default="")
    member = relationship("Member")

class WorkoutPlan(Base):
    __tablename__ = "workout_plans"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    trainer_id: Mapped[int | None] = mapped_column(ForeignKey("trainers.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(120))
    details: Mapped[str] = mapped_column(Text)
    start_date: Mapped[date] = mapped_column(Date, default=date.today)
    member = relationship("Member")
    trainer = relationship("Trainer")

class DietPlan(Base):
    __tablename__ = "diet_plans"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    trainer_id: Mapped[int | None] = mapped_column(ForeignKey("trainers.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(120))
    details: Mapped[str] = mapped_column(Text)
    start_date: Mapped[date] = mapped_column(Date, default=date.today)
    member = relationship("Member")
    trainer = relationship("Trainer")
