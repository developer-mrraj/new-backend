from fastapi import APIRouter, Depends, status, Response, HTTPException, Query
from .. import models, schemas
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional 



router= APIRouter()

@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.Categories).all()


@router.post("/categories")
def create_category(category: schemas.CategoryBase, db: Session = Depends(get_db)):
    db_category = models.Categories(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.post("/products")
def create_product(product: schemas.ProductBase, db: Session = Depends(get_db)):
    category = db.query(models.Categories).filter(models.Categories.category_id == product.Category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Invalid category ID")

    # Create product
    db_product = models.Products(**product.dict(exclude={"size", "color"}))
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    # Insert multiple sizes
    if product.size:
        db_sizes = [models.Size(size=s, product_id=db_product.product_id) for s in product.size]
        db.add_all(db_sizes)

    # Insert multiple colors
    if product.color:
        db_colors = [models.Color(color=c, product_id=db_product.product_id) for c in product.color]
        db.add_all(db_colors)

    db.commit()
    
    return db_product


@router.get("/products/{name}")
def get_product_by_name(name: str, db: Session = Depends(get_db)):
    product = db.query(models.Products).filter(models.Products.product_name == name).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {
        "product_id": product.product_id,
        "product_name": product.product_name,
        "price": product.price,
        "quantity": product.quantity,
        "category_id": product.Category_id
    }
