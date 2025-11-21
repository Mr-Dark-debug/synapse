from fastapi import FastAPI, Request
import time
from fastapi.middleware.cors import CORSMiddleware
from db.session import engine
from db import models
from api.routers import auth, user, research, collections, chat

# Create Database Tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Synapse API", description="Backend for Synapse Research Tool")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"[{request.method}] {request.url} - {response.status_code} - {process_time:.4f}s")
    return response

# Include Routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(research.router)
app.include_router(collections.router)
app.include_router(chat.router)

@app.get("/")
async def root():
    return {"message": "Synapse Hive Mind is Active"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
