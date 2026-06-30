from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# --- FAQ Schemas ---
class FAQBase(BaseModel):
    question: str
    answer: str

class FAQResponse(FAQBase):
    id: int

    class Config:
        from_attributes = True

# --- Product Schemas ---
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True

# --- Order Schemas ---
class OrderBase(BaseModel):
    customer_phone: str
    status: str
    total_price: float
    estimated_delivery: Optional[datetime] = None

class OrderResponse(OrderBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True