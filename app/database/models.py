from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_phone = Column(String(50), nullable=False, index=True)  # WhatsApp phone number
    status = Column(String(50), default="Pending")  # e.g., Shipped, Delivered, Processing
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    estimated_delivery = Column(DateTime, nullable=True)

class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(255), nullable=False, index=True)
    answer = Column(Text, nullable=False)
    
    
class Ticket(Base):
    __tablename__ = "ticket"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_phone = Column(String(50), nullable=False, index=True)
    issue_description = Column(Text, nullable=False)
    status = Column(String(50), default="Open") # Open, In Progress, Resolved
    created_at = Column(DateTime, default=datetime.utcnow)