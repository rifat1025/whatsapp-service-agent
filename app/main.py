import os
from fastapi import FastAPI, Request, Response, Depends, status, BackgroundTasks
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv

# Import our custom architecture components
from app.database.database import init_db
from app.agent.agent import get_whatsapp_agent
from app.services.whatsapp import send_whatsapp_message

load_dotenv()

app = FastAPI(title="WhatsApp AI Agent Service")

# Verify Token configured in Step 1 for Meta connection authorization
VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")
print(VERIFY_TOKEN)

@app.on_event("startup")
def on_startup():
    """Initializes the application by building missing MySQL database tables."""
    print("🚀 Booting database engines...")
    init_db()
    print("✅ MySQL Engine ready.")
    


@app.get("/webhook")
def verify_webhook(request: Request):
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("🌐 Webhook verified successfully by Meta!")
            # This must be an unquoted, plain text string returned to Meta
            return PlainTextResponse(content=challenge, status_code=status.HTTP_200_OK)
        
    # If token validation fails, return 403 as a plain text string
    return PlainTextResponse(
        content="Verification token mismatch", 
        status_code=status.HTTP_403_FORBIDDEN
    )

# 🔥 Background task execution pipeline

def process_agent_response(customer_phone: str, user_text: str):
    """
    এই ফাংশনটি ব্যাকগ্রাউন্ড থ্রেডে রান হবে। 
    এটি ল্যাংকচেইনের কাজ শেষ করে কাস্টমারকে হোয়াটসঅ্যাপে রিপ্লাই পাঠাবে।
    """
    try:
        print(f"🧠 Background processing started for {customer_phone}...")

        # ১. ফোন নম্বর দিয়ে এজেন্ট এবং তার চ্যাট হিস্ট্রি অবজেক্টটি নিয়ে আসা
        agent_executor, memory_history = get_whatsapp_agent(customer_phone)
        
        # ২. ডেটাবেজ থেকে এই ইউজারের আগের চ্যাট হিস্ট্রি রিড করা
        saved_messages = memory_history.messages
        
        # ৩. ল্যাংকচেইনের মাধ্যমে এআই রান করানো (পুরোনো হিস্ট্রি সহ)
        ai_response = agent_executor.invoke({
            "input": user_text,
            "chat_history": saved_messages 
        })
        
        reply_text = ai_response.get("output", "আই অ্যাম সরি, আমি এই মুহূর্তে তথ্যটি প্রসেস করতে পারছি না।")
        
        # ৪. কাস্টমারের মেসেজ এবং এআই এর উত্তর ডেটাবেজে মেমোরি হিসেবে সেভ করা
        memory_history.add_user_message(user_text)
        memory_history.add_ai_message(reply_text)
        
        # ۵. মেটা ক্লাউড এপিআই এর মাধ্যমে কাস্টমারকে মেসেজ পাঠানো
        send_whatsapp_message(customer_phone, reply_text)
        print(f"🤖 Successfully replied to {customer_phone}")

    except Exception as e:
        print(f"❌ Error inside background process_agent_response: {str(e)}")

@app.post("/webhook")
async def receive_whatsapp_message(request: Request, background_tasks: BackgroundTasks):
    """
    হোয়াটসঅ্যাপ থেকে আসা রিয়েল-টাইম মেসেজ হ্যান্ডেল করার মূল পোস্ট রুট।
    """
    body = await request.json()
    
    # 1. Drop anything that isn't a WhatsApp account update immediately
    if body.get("object") != "whatsapp_business_account":
        return Response(content="NOT_WHATSAPP", status_code=status.HTTP_400_BAD_REQUEST)

    try:
        for entry in body.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                
                # 🔥 GUARD 1: If it's a delivery status update (sent/delivered/read), skip it completely
                if "statuses" in value:
                    continue
                
                # Process actual incoming messages
                if "messages" in value:
                    for msg in value["messages"]:
                        customer_phone = msg.get("from")
                        msg_type = msg.get("type")
                        
                        # Handle text messages
                        if msg_type == "text":
                            user_text = msg["text"]["body"]
                            print(f"📩 Text from {customer_phone}: '{user_text}'")
                            
                            # 🔥 FIX: AI task ti non-blocking background threads e pathiye deya holo
                            background_tasks.add_task(process_agent_response, customer_phone, user_text)
                            
                        # 🔥 GUARD 2: Catch media/interactive items
                        else:
                            print(f"⚠️ Received unhandled message type '{msg_type}' from {customer_phone}")

    except Exception as e:
        print(f"❌ Error compiling webhook message data pipeline: {str(e)}")
        
    # Meta response rapidly chole jabe ekhon (<50ms)
    return Response(content="EVENT_RECEIVED", status_code=status.HTTP_200_OK)