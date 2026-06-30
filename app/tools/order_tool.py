from langchain_core.tools import tool
from app.database.database import SessionLocal
from app.database.models import Order

@tool
def order_tracking_tool(customer_phone: str) -> str:
    """
    Tracks the status of an order using the customer's phone number.
    Use this whenever a user wants to know where their package is or its status.
    """
    db = SessionLocal()
    try:
        # Get the latest order for this phone number
        order = db.query(Order).filter(Order.customer_phone == customer_phone).order_by(Order.created_at.desc()).first()
        
        if not order:
            return f"No orders found associated with the phone number {customer_phone}."
        
        delivery_str = f"Estimated Delivery: {order.estimated_delivery.strftime('%Y-%m-%d')}" if order.estimated_delivery else ""
        return (
            f"📦 *Order #{order.id} Status*:\n"
            f"• Status: {order.status}\n"
            f"• Total: ${order.total_price:.2f}\n"
            f"• Ordered on: {order.created_at.strftime('%Y-%m-%d')}\n"
            f"{delivery_str}"
        )
    except Exception as e:
        return f"Error tracking order: {str(e)}"
    finally:
        db.close()