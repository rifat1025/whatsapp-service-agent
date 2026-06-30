# 📱 WhatsApp AI E-Commerce Agent

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/LangChain-ReAct-green.svg" alt="LangChain">
  <img src="https://img.shields.io/badge/Groq-Llama%203.1-orange.svg" alt="Groq">
  <img src="https://img.shields.io/badge/MySQL-Database-4479A1.svg" alt="MySQL">
  <img src="https://img.shields.io/badge/License-MIT-success.svg" alt="MIT">
</p>

<p align="center">
An enterprise-grade <strong>WhatsApp AI Agent</strong> built with <strong>FastAPI</strong>, <strong>LangChain</strong>, <strong>Groq llama-3.3-70b-versatile</strong>, and <strong>MySQL</strong> for intelligent e-commerce automation.
</p>

---

# 🚀 Overview

This project is a production-ready AI-powered WhatsApp assistant that enables customers to interact directly through WhatsApp without requiring a traditional website or mobile application.

The agent understands natural language, autonomously selects the appropriate tools using the **ReAct** reasoning framework, retrieves live information from a MySQL database, and responds with accurate, context-aware answers.

Instead of generating fabricated responses, the agent performs real database queries for products, orders, FAQs, and customer support requests.

Typical customer requests include:

- 🔍 Product Search
- 📦 Order Tracking
- ❓ FAQ Answering
- 🎫 Support Ticket Creation
- 💬 Context-Aware Conversations

---

# ✨ Features

### 🤖 AI-Powered Reasoning

- Uses **LangChain ReAct Agent**
- Autonomous tool selection
- Multi-step reasoning
- Context-aware conversations

---

### 🛍️ Product Search

- Search products using natural language
- Check product availability
- View stock status
- Retrieve pricing information
- Recommend matching products

Example:

> "Do you have a gaming mouse under $40?"

---

### 📦 Order Tracking

Customers can simply send:

> "Track my order"

The AI retrieves:

- Order status
- Estimated delivery
- Shipping updates

directly from the database.

---

### ❓ FAQ Assistant

Instantly answers frequently asked questions such as:

- Shipping information
- Payment methods
- Return policy
- Business hours
- Warranty

---

### 🎫 Human Support Escalation

If a customer requests:

- Refund
- Complaint
- Exchange
- Human support

the AI automatically creates a support ticket inside MySQL for follow-up by a customer support representative.

---

### 💾 Persistent Chat Memory

Uses:

- SQLChatMessageHistory
- MySQL

to maintain conversation history, enabling more natural and context-aware interactions.

---

### ⚡ Fast Webhook Processing

Meta requires webhook responses within a few seconds.

This project immediately acknowledges webhook events while processing AI tasks asynchronously using FastAPI BackgroundTasks, ensuring low latency and preventing webhook timeouts.

---

# 🏗️ Tech Stack

| Category | Technology |
|-----------|------------|
| Language | Python 3.10 |
| Backend | FastAPI |
| AI Framework | LangChain |
| LLM | Groq (llama-3.3-70b-versatile) |
| Agent Pattern | ReAct |
| Database | MySQL |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Messaging | WhatsApp Business Cloud API |
| Deployment | Uvicorn |

---

# 📂 Project Structure

```text
.
├── app
│
├── agent
│   └── agent.py
│
├── database
│   ├── database.py
│   ├── models.py
│   └── schemas.py
│
├── services
│   └── whatsapp.py
│
├── tools
│   ├── faq_tool.py
│   ├── order_tool.py
│   ├── product_tool.py
│   └── ticket_tool.py
│
├── main.py
│
├── requirements.txt
│
└── README.md
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/your-username/whatsapp-ai-agent.git

cd whatsapp-ai-agent
```

---

## 2. Create Virtual Environment

### Linux / macOS

```bash
python3.10 -m venv venv

source venv/bin/activate
```

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file.

```env
###################################
# Groq API
###################################

GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxx

###################################
# Database
###################################

DATABASE_URL=mysql+pymysql://root:password@localhost:3306/whatsapp_agent_db

###################################
# WhatsApp Cloud API
###################################

WHATSAPP_TOKEN=EAABxxxxxxxxxxxxxxxxxxxxx

WHATSAPP_PHONE_NUMBER_ID=1234567890

WHATSAPP_VERIFY_TOKEN=my_secure_verify_token
```

---

# 🗄️ Database

The application automatically creates database tables during startup.

You can insert sample data for testing.

## Products

```sql
INSERT INTO products
(name, description, price, stock)

VALUES

('Logitech G304 Mouse',
'Wireless Gaming Mouse',
35.00,
10),

('Mechanical Keyboard',
'RGB Blue Switch Keyboard',
45.00,
0);
```

---

## FAQs

```sql
INSERT INTO faqs

(question, answer)

VALUES

(
'shipping time',
'Delivery takes 24-48 hours inside Dhaka and 3-5 days outside.'
),

(
'payment methods',
'We accept bKash, Nagad, Rocket and Cash on Delivery.'
);
```

---

# ▶️ Running the Application

Development mode

```bash
uvicorn app.main:app --reload
```

Production mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

# 🧪 Local Testing

## Product Search

```bash
curl -X POST http://127.0.0.1:8000/webhook \
-H "Content-Type: application/json" \
-d '{
  "object": "whatsapp_business_account",
  "entry": [{
    "changes": [{
      "value": {
        "messages": [{
          "from": "8801700000000",
          "type": "text",
          "text": {
            "body": "Do you have any gaming mouse available?"
          }
        }]
      },
      "field": "messages"
    }]
  }]
}'
```

---

## Refund Request

```bash
curl -X POST http://127.0.0.1:8000/webhook \
-H "Content-Type: application/json" \
-d '{
  "object": "whatsapp_business_account",
  "entry": [{
    "changes": [{
      "value": {
        "messages": [{
          "from": "8801700000000",
          "type": "text",
          "text": {
            "body": "I want a refund for my order."
          }
        }]
      },
      "field": "messages"
    }]
  }]
}'
```

---

# 🌐 Deploying with Meta WhatsApp Cloud API

## Step 1

Start your FastAPI server.

```bash
uvicorn app.main:app --reload
```

---

## Step 2

Expose your local server using ngrok.

```bash
ngrok http 8000
```

---

## Step 3

Open the Meta Developer Dashboard.

Navigate to:

```
WhatsApp App

↓

Configuration

↓

Webhooks
```

---

## Step 4

Configure

**Callback URL**

```
https://your-ngrok-url.ngrok-free.app/webhook
```

**Verify Token**

```
my_secure_verify_token
```

(The value must exactly match the value in your `.env` file.)

---

## Step 5

Subscribe to

```
messages
```

---

## Step 6

Send a message from your WhatsApp test phone.

Example:

```
Hi

Do you have gaming mouse?

Track my order

What payment methods do you support?

I want a refund.
```

The AI Agent will automatically process the request and respond.

---

# 🔄 Workflow

```text
Customer
      │
      ▼
WhatsApp
      │
      ▼
Meta Cloud API
      │
      ▼
FastAPI Webhook
      │
      ▼
Background Task
      │
      ▼
LangChain ReAct Agent
      │
      ▼
───────────────
│ Product Tool │
│ Order Tool   │
│ FAQ Tool     │
│ Ticket Tool  │
───────────────
      │
      ▼
MySQL Database
      │
      ▼
AI Response
      │
      ▼
WhatsApp Customer
```

---

# 📌 Future Improvements

- Payment Integration
- RAG with Vector Database
- Product Recommendation Engine
- Voice Message Support
- Image-Based Product Search
- Admin Dashboard
- Analytics Dashboard
- Multi-language Support
- Docker Deployment
- Kubernetes Support
- Redis Caching
- Authentication & Authorization

---

# 🤝 Contributing

Contributions are welcome!

If you have ideas for improvements, feel free to:

- Fork the repository
- Create a feature branch
- Commit your changes
- Open a Pull Request

---

# 📄 License

This project is licensed under the **MIT License**.

Feel free to use, modify, and distribute this project in accordance with the license.

---

# 👨‍💻 Author

**Rifat Sarker**

AI Engineer | Machine Learning | NLP | LangChain | FastAPI | Computer Vision

If you found this project helpful, consider giving it a ⭐ on GitHub.
