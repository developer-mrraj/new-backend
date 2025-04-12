from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    mobile_number = Column(String(15), unique=True)  # Changed to String with max length
    email = Column(String(255), unique=True, index=True)
    address = Column(String(500))  # Increased size for full addresses
    
    # Use 'items' as the relationship name
    items = relationship("Items", back_populates="customer") 
    billings = relationship("Billing", back_populates="customer") 

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))  # Ensure to hash before storing

class Billing(Base):
    __tablename__ = 'billing'
    
    bill_id = Column(String(255),primary_key=True,index=True)
    current_date = Column(String(50))
    payment_method = Column(String(50))
    
        # Foreign key to link with the Customer table
    customer_id = Column(Integer, ForeignKey('customer.id'))

    # Relationship with Customer
    customer = relationship("Customer", back_populates="billings")
    items = relationship("Items", back_populates="billing") 
    
class Items(Base):
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    quantity = Column(Integer)
    price  = Column(Integer)
    discount  = Column(Integer)
    total  = Column(Integer)
    
    # Foreign key to link with the Customer table
    customer_id = Column(Integer, ForeignKey('customer.id'))
    bill_id = Column(String(255),ForeignKey('billing.bill_id'))

    # Relationship with Customer
    customer = relationship("Customer", back_populates="items")
    billing = relationship("Billing", back_populates="items")
    

    
class Categories(Base):
    __tablename__='categories'
    
    category_id = Column(Integer,primary_key=True)
    category_name = Column(String(255), unique=True)
    
    products = relationship("Products", back_populates="category")

class Products(Base):
    __tablename__='products'
    
    product_id = Column(Integer, primary_key=True, index=True)
    product_code = Column(String(255), unique=True)
    product_name = Column(String(255))
    quantity = Column(Integer)
    product_price = Column(Integer)
    Category_id = Column(Integer, ForeignKey('categories.category_id'))
    
    category = relationship("Categories", back_populates="products")
    size = relationship("Size", back_populates="products")
    color = relationship("Color", back_populates="products")
    

    
class Size(Base):
    __tablename__='size'
    
    size_id = Column(Integer,primary_key=True,index=True)
    size = Column(String(255))
    product_id = Column(Integer, ForeignKey('products.product_id'))
    
    products = relationship("Products", back_populates="size")
    

class Color(Base):
    __tablename__='color'
    
    color_id = Column(Integer, primary_key=True, index=True)
    color = Column(String(255))
    product_id = Column(Integer, ForeignKey('products.product_id'))
    
    products = relationship("Products", back_populates="color")
    
    


    # color_id INT AUTO_INCREMENT PRIMARY KEY,
    # product_id INT,
    # color VARCHAR(50) NOT NULL,
    # FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE