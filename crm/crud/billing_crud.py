from sqlalchemy.orm import Session
from ..models import Billing
from ..schemas import BillingRequest
import random
import string
from datetime import datetime

def generate_bill_id():
    prefix = "BILL"
    random_number = ''.join(random.choices(string.digits, k=5))
    return f"{prefix}{random_number}"

def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

def create_billing(db: Session, customer_id: int, billing: BillingRequest):
    new_billing = Billing(
        bill_id=billing.bill_id,
        current_date=billing.current_date,
        payment_method=billing.payment_method,
        customer_id=customer_id
    )
    db.add(new_billing)
    db.commit()
    db.refresh(new_billing)
    return {"message": "Billing record created successfully!"}
