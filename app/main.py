from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .admin import setup_admin
from .routers import wallets, auth

app = FastAPI(title="HD Wallet Dashboard")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(wallets.router, prefix="/api")

setup_admin(app)

@app.get("/")
def root():
    return {"message": "API Running → /admin for dashboard, /docs for Swagger"}
