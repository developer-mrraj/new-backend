from fastapi import FastAPI, Depends, HTTPException
from . import models
from .database import engine
from .routers import  customers_router, inventory_router, items_router, authentication, billing_routers, users, sales
from fastapi.middleware.cors import CORSMiddleware



app =  FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Allows all origins (change to ["http://localhost:4200"] for security)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

models.Base.metadata.create_all(bind=engine)

app.include_router(authentication.router)
app.include_router(customers_router.router)
app.include_router(billing_routers.router)
app.include_router(users.router)
app.include_router(sales.router)
app.include_router(inventory_router.router)
# app.include_router(items_router.router)

