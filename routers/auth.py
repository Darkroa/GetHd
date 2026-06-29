from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from ..database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Simple demo auth (username: admin, password: admin123)
    if form_data.username != "admin" or form_data.password != "admin123":
        raise HTTPException(status_code=400, detail="Incorrect credentials")
    
    from ..routers.auth import create_access_token  # avoid circular
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}