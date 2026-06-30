from langchain_core.tools import tool
from app.database.database import SessionLocal
from app.database.models import FAQ

@tool
def faq_search_tool(query: str) -> str:
    """
    Searches the FAQ knowledge base for questions or topics.
    Use this to answer questions about return policies, business hours, and shipping details.
    """
    db = SessionLocal()
    try:
        # Simple text matching on the question column
        faqs = db.query(FAQ).filter(FAQ.question.like(f"%{query}%")).all()
        
        if not faqs:
            return "No matching FAQ entries found. Try rephrasing your question."
            
        results = [f"❓ *{f.question}*\n💬 {f.answer}" for f in faqs]
        return "\n\n".join(results)
    except Exception as e:
        return f"Error searching FAQs: {str(e)}"
    finally:
        db.close()