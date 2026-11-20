from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import Base, engine
from app.routers import auth, members, trainers, memberships, payments, attendance, fitness, dashboard

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app=FastAPI(title=settings.APP_NAME,version="1.0.0",description="Full-stack gym operations management API",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=settings.CORS_ORIGINS if settings.CORS_ORIGINS != ["*"] else ["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

for router in [auth.router,members.router,trainers.router,memberships.router,payments.router,attendance.router,fitness.router,dashboard.router]:
    app.include_router(router)

@app.get("/")
def root():
    return {"message":"FitFlow Gym Management API is running","docs":"/docs","health":"/health"}

@app.get("/health")
def health():
    return {"status":"ok"}
