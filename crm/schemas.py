from pydantic import BaseModel
from typing import List, Optional

        
class ItemBase(BaseModel):
    name: str
    quantity: int
    price: int
    discount: int
    total: int

    class Config:
        from_attributes = True

class ItemCreate(ItemBase):
    pass  # No need to include customer_id here; we'll set it automatically

class Item(ItemBase):
    id: int
    customer_id: int
    bill_id:str

class CustomerBase(BaseModel):
    name: str
    mobile_number: int
    email: str
    address: str

    class Config:
        from_attributes = True

class CustomerCreate(CustomerBase):
    pass

class CustomerWithItems(CustomerBase):
    id: int
    items: List[Item] = []
    
# Schema for billing
class BillingRequest(BaseModel):
    bill_id: str
    current_date: str
    payment_method: str

    class Config:
        from_attributes = True
        
class Bill(BillingRequest):
    customer_id: int



class User(BaseModel):
    name: str
    email: str
    password: str
    
class Login(BaseModel):
    username :str
    password :str
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    
class CategoryBase(BaseModel):
    category_id: int
    category_name: str

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    product_code: str
    product_name: str
    quantity: int
    product_price: int
    Category_id: int
    size: List[str] = []  # Ensure this is a list, not a string
    color: List[str] = []

    class Config:
        from_attributes = True
        
    