from fastapi import APIRouter, Depends
from .. import schemas, models, hashing
from sqlalchemy.orm import Session
from ..database import get_db



router = APIRouter(
    tags=["users"]
)

# User means Business Owner

@router.post('/user')
def create_user(request:schemas.User,db:Session = Depends(get_db)):
     new_user= models.User(name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password))
     db.add(new_user)
     db.commit()
     db.refresh(new_user)
     return new_user
