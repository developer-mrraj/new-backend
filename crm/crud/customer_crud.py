from sqlalchemy.orm import Session
from ..models import Customer, Items, Billing
from ..schemas import CustomerBase, ItemCreate, BillingRequest
from typing import List,Optional

def get_customers(db: Session, name: Optional[str] = None, customer_id: Optional[int] = None) -> List[Customer]:
    query = db.query(Customer)

    if name:
        query = query.filter(Customer.name.ilike(f"%{name}%"))  # Case-insensitive search

    if customer_id:
        query = query.filter(Customer.id == customer_id)  # Exact match for ID

    return query.all()

def create_customer(db: Session, customer: CustomerBase):
    existing_customer = db.query(Customer).filter(Customer.email == customer.email).first()

    if not existing_customer:
        new_customer = Customer(name=customer.name, email=customer.email)
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
        return new_customer
    return existing_customer

def create_items(db: Session, customer_id: int, items: List[ItemCreate]):
    item_objs = [Items(name=item.name, quantity=item.quantity, price=item.price, customer_id=customer_id) for item in items]
    db.add_all(item_objs)
    db.commit()
    return item_objs

def create_billing(db: Session, customer_id: int, billing: BillingRequest):
    new_billing = Billing(
        bill_id=billing.bill_id,
        current_date=billing.current_date,
        payment_method=billing.payment_method,
        customer_id=customer_id
    )
    db.add(new_billing)
    db.commit()
    return new_billing

def create_customer_with_items_and_billing(
    db: Session,
    customer: CustomerBase,
    items: List[ItemCreate],
    billing: BillingRequest
):
    # Step 1: Create or get customer
    new_customer = create_customer(db, customer)

    # Step 2: Create items linked to the customer
    create_items(db, new_customer.id, items)

    # Step 3: Create billing linked to the customer
    create_billing(db, new_customer.id, billing)

    return {"message": "Customer, items, and billing created successfully!"}
