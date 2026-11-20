from datetime import date, datetime
from pydantic import BaseModel, EmailStr, ConfigDict, Field

class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class RegisterIn(BaseModel):
    full_name: str
    email: EmailStr
    password: str = Field(min_length=8)
    role: str = "member"

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class UserOut(ORMModel):
    id: int
    full_name: str
    email: EmailStr
    role: str
    is_active: bool

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

class MemberIn(BaseModel):
    full_name: str
    email: EmailStr
    phone: str = ""
    age: int = 18
    gender: str = "Prefer not to say"
    joined_on: date | None = None
    is_active: bool = True
    notes: str = ""

class MemberOut(ORMModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str
    age: int
    gender: str
    joined_on: date
    is_active: bool
    notes: str

class TrainerIn(BaseModel):
    full_name: str
    email: EmailStr
    phone: str = ""
    specialization: str = "General Fitness"
    experience_years: int = 0
    is_active: bool = True

class TrainerOut(ORMModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str
    specialization: str
    experience_years: int
    is_active: bool

class PlanIn(BaseModel):
    name: str
    duration_days: int
    price: float
    description: str = ""
    is_active: bool = True

class PlanOut(ORMModel):
    id: int
    name: str
    duration_days: int
    price: float
    description: str
    is_active: bool

class MembershipIn(BaseModel):
    member_id: int
    plan_id: int
    trainer_id: int | None = None
    start_date: date | None = None

class MembershipOut(ORMModel):
    id: int
    member_id: int
    plan_id: int
    trainer_id: int | None
    start_date: date
    end_date: date
    status: str

class PaymentIn(BaseModel):
    member_id: int
    membership_id: int | None = None
    amount: float
    payment_date: date | None = None
    method: str = "Cash"
    status: str = "paid"
    reference: str = ""

class PaymentOut(ORMModel):
    id: int
    member_id: int
    membership_id: int | None
    amount: float
    payment_date: date
    method: str
    status: str
    reference: str

class AttendanceIn(BaseModel):
    member_id: int
    notes: str = ""

class AttendanceOut(ORMModel):
    id: int
    member_id: int
    check_in: datetime
    check_out: datetime | None
    notes: str

class PlanAssignmentIn(BaseModel):
    member_id: int
    trainer_id: int | None = None
    title: str
    details: str
    start_date: date | None = None

class PlanAssignmentOut(ORMModel):
    id: int
    member_id: int
    trainer_id: int | None
    title: str
    details: str
    start_date: date
