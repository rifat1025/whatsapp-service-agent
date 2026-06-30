# app/tools/ticket_tool.py

from langchain_core.tools import tool
from app.database.database import SessionLocal
from app.database.models import Ticket

@tool
def create_support_ticket_tool(customer_phone: str, issue_description: str) -> str:
    """
    Creates a support ticket in the MySQL database when a customer has a complaint, 
    wants a refund, or requests human agent assistance.
    Input requires the customer's phone number and a brief summary of their issue.
    """
    db = SessionLocal()
    try:
        # ডেটাবেজে নতুন টিকিট রো তৈরি করা
        new_ticket = Ticket(
            customer_phone=customer_phone,
            issue_description=issue_description,
            status="Open"
        )
        db.add(new_ticket)
        db.commit()
        db.refresh(new_ticket)
        
        return (
            f"🎟️ *Support Ticket Created Successfully!*\n"
            f"• Ticket ID: #{new_ticket.id}\n"
            f"• Issue: {new_ticket.issue_description}\n"
            f"• Status: {new_ticket.status}\n"
            f"আমাদের একজন প্রতিনিধি খুব শীঘ্রই আপনার সাথে যোগাযোগ করবেন।"
        )
    except Exception as e:
        db.rollback()
        return f"Error creating support ticket: {str(e)}"
    finally:
        db.close()