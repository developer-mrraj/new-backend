from sqlalchemy.orm import Session
from ..models import Items
from ..schemas import ItemCreate,ItemBase
from typing import List

def create_items(db: Session, customer_id: int, items: List[ItemBase]):
    item_objs = [Items(**item.dict(), customer_id=customer_id) for item in items]  # Use unpacking to simplify
    db.add_all(item_objs)
    db.commit()
    db.refresh(item_objs)
    return {"message": "Items added successfully!", "items": item_objs}

