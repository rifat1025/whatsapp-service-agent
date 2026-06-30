from dotenv import load_dotenv
from langchain_community.chat_message_histories import SQLChatMessageHistory
import os
from app.tools.faq_tool import faq_search_tool
from app.tools.order_tool import order_tracking_tool
from app.tools.product_tool import product_search_tool

from app.tools.ticket_tool import create_support_ticket_tool

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
import json
from langchain_groq import ChatGroq



load_dotenv()

def get_whatsapp_agent(customer_phone : str):
    
    
    llm= ChatGroq(model="llama-3.3-70b-versatile",temperature=0)
    # 2. Register our custom database tools
    tools = [
        product_search_tool,
        order_tracking_tool,
        faq_search_tool,
        create_support_ticket_tool 
    ]
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are a concise e-commerce WhatsApp assistant. Your tasks:\n"
            "- Answer product questions using 'product_search_tool'.\n"
            "- Track packages using 'order_tracking_tool'.\n"
            "- Answer policies/FAQs using 'faq_search_tool'.\n\n"
            "CRITICAL: Always use the appropriate tool to fetch facts before responding. "
            "Keep answers short, use bullet points and emojis. Do not invent details."
        )),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    # 4. Bind everything into a structured tool-calling agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    chat_history = SQLChatMessageHistory(
        session_id = customer_phone,
        connection_string=os.getenv("DATABASE_URL"),
        table_name="message_store"
    )
    # 5. Return the execution framework
    return AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True,  # Will display reasoning steps beautifully in your terminal logs
        handle_parsing_errors=True
    ),chat_history
    



