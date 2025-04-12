from fastapi import APIRouter, Depends, status, Response, HTTPException, Query
from .. import models, schemas
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional, List
from ..oauth2 import get_current_user
from ..crud import customer_crud

# from fastapi import FastAPI


# app =  FastAPI()

router = APIRouter()


# current_user: schemas.User = Depends(get_current_user)==> for authorization
@router.get('/get')
def get_customers(
    db: Session = Depends(get_db),
    name: Optional[str] = Query(None),  # Optional query param for name
    customer_id: Optional[int] = Query(None)  # Optional query param for ID
):
    query = db.query(models.Customer)

    if name:
        query = query.filter(models.Customer.name.ilike(f"%{name}%"))  # Case-insensitive search

    if customer_id:
        query = query.filter(models.Customer.id == customer_id)  # Exact match for ID

    customers = query.all()
    return customers 


@router.get("/check-customer/")
def check_customer(email: str = None, mobile_number: int = None, db: Session = Depends(get_db)):
    existing_customer = db.query(models.Customer).filter(
        (models.Customer.email == email) | (models.Customer.mobile_number == mobile_number)
    ).first()

    return existing_customer if existing_customer else None


# @router.get('/{id}')
# def show(id, db:Session = Depends(get_db)):
#     users = db.query(models.Users).filter(models.Users.id == id).first()
#     if not users:
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {'detail':f'blog with the id with {id} is not found'}
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail= f'blog with the id with {id} is not available' )
#     return users

# current_user: schemas.User = Depends(get_current_user) it checks that the user is valide or not who is try to access this post request 


# ,current_user: schemas.User = Depends(get_current_user) for authorization

@router.post("/customers/")
def create_customer(
    customer: schemas.CustomerBase, 
    items: List[schemas.ItemCreate], 
    billing: schemas.BillingRequest, 
    db: Session = Depends(get_db)
):
    # Check if the customer already exists
    existing_customer = db.query(models.Customer).filter(
        models.Customer.email == customer.email
    ).first()

    if existing_customer:
        db_customer = existing_customer
    else:
        db_customer = models.Customer(**customer.dict())
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)

    # Create a new billing record
    new_bill = models.Billing(
        bill_id=billing.bill_id,
        current_date=billing.current_date,
        payment_method=billing.payment_method,
        customer_id=db_customer.id
    )
    db.add(new_bill)
    db.commit()
    db.refresh(new_bill)  # Ensure it gets a proper ID before linking items

    # Add items linked to the customer's ID and the new bill_id
    item_objs = []

    for item in items:
        # 🔍 Filter product by name
        product = db.query(models.Products).filter(models.Products.product_name == item.name).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product '{item.name}' not found.")

        if product.quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for product '{product.product_name}'. Available: {product.quantity}, Requested: {item.quantity}"
            )

        # Update product quantity
        product.quantity -= item.quantity
        db.add(product)

        # Total calculation
        discounted_price = item.price - (item.discount or 0)
        total = item.quantity * discounted_price

        item_obj = models.Items(
            name=product.product_name,
            quantity=item.quantity,
            price=item.price,
            discount=item.discount,
            total=total,
            customer_id=db_customer.id,
            bill_id=new_bill.bill_id
        )
        item_objs.append(item_obj)

    db.add_all(item_objs)
    db.commit()

    return {
        "customer_id": db_customer.id,
        "bill_id": new_bill.bill_id,
        "message": "Customer and billing created successfully"
    }




# @router.put('/update/{id}')
# def UpdateUser(id:int, request:schemas.Customer,db:Session = Depends(get_db)):
#     customers= db.query(models.Customer).filter(models.Customer.id == id).first()
#     if not customers:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'id with {id} not present')
#     customers.name = request.name
#     customers.mobile_number = request.mobile_number
#     customers.email = request.email
#     customers.product_name = request.product_name
#     customers.price = request.price
#     customers.address = request.address
#     db.commit()
#     return 'updated'
    
    
# @router.delete('/delete/{id}')
# def deleteUsers(id:int,db:Session = Depends(get_db)):
#     customers= db.query(models.Customer).filter(models.Customer.id == id).delete()
#     db.commit()
#     return customers
