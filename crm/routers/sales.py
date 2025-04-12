from fastapi import FastAPI, Query, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db  # Import your database session
from ..models import Billing, Items  # Import SQLAlchemy models
from sqlalchemy import func, cast, Date
from datetime import datetime, timedelta

router = APIRouter()

# @router.get("/sales")
# def get_sales(days: int = Query(7, description="Get sales for the last X days"), db: Session = Depends(get_db)):
#     # Calculate start date based on the number of days requested
#     start_date = datetime.now() - timedelta(days=days)

#     # Query to get total sales per day, summing up all items per billing date
#     sales_data = (
#         db.query(
#             func.date(Billing.current_date).label("sales_date"),  
#             func.sum(Items.total).label("total_sales")
#         )
#         .join(Items, Billing.bill_id == Items.bill_id)
#         .filter(Billing.current_date >= start_date)  # Compare directly
#         .group_by(func.date(Billing.current_date))
#         .order_by(func.date(Billing.current_date).desc())
#         .all()
#     )

#     # Debugging output
#     print("Fetched Sales Data:", sales_data)

#     return {
#         "sales": [
#             {"date": sale.sales_date, "total_sales": sale.total_sales}
#             for sale in sales_data
#         ]
#     }
