from langchain_core.tools import tool
from app.database.database import SessionLocal
from app.database.models import Product 

@tool(description="Search for products in the inventory using a text query.")
def product_search_tool(query: str) -> str:
    
    
    db = SessionLocal()
    
    try:
        products = db.query(Product).filter(Product.name.like(f"%{query}%")).all()
        
        if not products :
            return f"No products found matching '{query}'."
        results = []
        for p in products:
            status = "In Stock" if p.stock > 0 else "Out of Stock"
            results.append(f"- *{p.name}*: ${p.price:.2f} ({status}) | {p.description}")
            
        return "Here is what I found:\n" + "\n".join(results)
    except Exception as e:
        return f"Error searching products: {str(e)}"
    finally:
        db.close()
            
    