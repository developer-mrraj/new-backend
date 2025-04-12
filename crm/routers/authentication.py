from datetime import timedelta
from fastapi import APIRouter , Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, models
from ..database import get_db
from sqlalchemy.orm import Session
from ..hashing import Hash
from ..token import create_access_token, create_refresh_token, REFRESH_TOKEN_EXPIRE_DAYS


router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first() #find the user in database
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalide Credentioals')
    # verify passwords
    if not Hash.verify(request.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalide-Password')
    
    
    #if login done successfully generate token
    access_token = create_access_token(data={"sub": user.email})
   

    refresh_token = create_refresh_token(
        data={"sub": user.email},
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    return {"access_token":access_token,"refresh_token": refresh_token, "token_type":"bearer"}