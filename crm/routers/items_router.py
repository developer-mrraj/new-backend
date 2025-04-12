from fastapi import APIRouter, Depends, status, Response, HTTPException, Query
from .. import models, schemas
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional, List
from ..crud import items_crud


router= APIRouter()


@router.post("/item/{customer_id}")
def add_items(customer_id: int, items: List[schemas.ItemBase], db: Session = Depends(get_db)):
    return items_crud.create_items(db, customer_id, items)
