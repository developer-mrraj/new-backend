from fastapi import APIRouter,Depends
from datetime import datetime
from .. import schemas,models
from sqlalchemy.orm import Session
from ..database import get_db
# random and string are the python libraries
import random
import string
from ..crud import billing_crud

router = APIRouter()

def generate_bill_id():
    prefix = "BILL"
    # The function random.choices(string.digits, k=5) selects 5 random digits from 0-9.
    random_number = ''.join(random.choices(string.digits, k=5))
    return f"{prefix}{random_number}"

def get_current_date():
    # datetime.now() gets the current date and time of your system.
    # strftime stands for "String Format Time"
    return datetime.now().strftime("%Y-%m-%d") 
    # return "2024-03-26"

# always get data in json format it will easier to interact with frontend 
@router.get("/get-new-bill-id")
def get_new_bill_id():
    bill_id = generate_bill_id()
    current_date = get_current_date()
    return {"bill_id": bill_id, "current_date": current_date}



@router.post("/biiling/{customer_id}")
def create_billing(customer_id: int, billing: schemas.BillingRequest, db: Session = Depends(get_db)):
    return billing_crud.create_billing(db, customer_id, billing)