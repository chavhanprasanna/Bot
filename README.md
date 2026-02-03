# Customer Support AI Chatbot for Agencies

An end-to-end SaaS starter that answers FAQs, creates support tickets, and escalates to humans using the **Groq free API** with **LLaMA3 (llama3-8b-8192)**. The project includes a FastAPI backend, Telegram + Discord bots, and a React/Tailwind admin dashboard.

## ✅ MVP Promise
> "This bot handled 100+ support tickets while I slept"

## Features
- FAQ knowledge base answering
- Automatic ticket creation with MongoDB Atlas Free Tier
- Escalation for sensitive or angry messages
- Telegram and Discord integrations
- Admin dashboard for ticket management
- Ticket status tracking: Open, Pending, Resolved, Escalated

## Tech Stack
- **Backend:** FastAPI, LangChain, Groq (LLaMA3), MongoDB Atlas
- **Bots:** Telegram Bot API, Discord Bot API
- **Frontend:** React + Tailwind CSS
- **Deployment:** Render (backend), Vercel (frontend)

---

## Project Structure
```
/backend
  main.py
  config.py
  db.py
  requirements.txt
  /models
  /routes
  /services
/bots
  telegram_bot.py
  discord_bot.py
/frontend
  index.html
  package.json
  vite.config.js
  tailwind.config.js
  postcss.config.js
  /src
README.md
.env.example
```

---

## ✅ Local Setup

### 1. Clone and configure environment
```bash
cp .env.example .env
```
Fill in:
- `GROQ_API_KEY`
- `MONGO_URI`
- `TELEGRAM_BOT_TOKEN`
- `DISCORD_BOT_TOKEN`

### 2. Backend (FastAPI)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

### 3. Frontend (Admin Dashboard)
```bash
cd frontend
npm install
npm run dev
```
Open: `http://localhost:5173`

### 4. Telegram Bot
```bash
cd bots
python telegram_bot.py
```

### 5. Discord Bot
```bash
cd bots
python discord_bot.py
```
Use command format:
```
!support My payment failed
```

---

## ✅ Demo Script (Showcase)
**User:** "My payment failed"  
**Bot:** Responds from FAQ or creates a ticket  
**User:** "I'm angry, I want a human"  
**Bot:** Escalates immediately and summarizes issue  

---

## LangChain + Groq (No OpenAI APIs)
```python
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama3-8b-8192",
    api_key=os.getenv("GROQ_API_KEY")
)
```

---

## Deployment Guide (Free Tier)

### Backend on Render
1. Create a new Web Service from GitHub
2. Set build command:
   ```
   pip install -r backend/requirements.txt
   ```
3. Set start command:
   ```
   uvicorn backend.main:app --host 0.0.0.0 --port 10000
   ```
4. Add environment variables from `.env`

### Frontend on Vercel
1. Import repo into Vercel
2. Set root directory to `/frontend`
3. Set env variable:
   ```
   VITE_API_URL=https://your-render-backend-url
   ```

---

## FAQ Setup
Insert FAQs with:
```bash
curl -X POST http://localhost:8000/faqs \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I reset my password?", "answer": "Click reset link"}'
```

---

## Monetization Potential
**Target:** Agencies spending $500–$2K/month on support staff  
**Pricing:** $2,000–$5,000/month based on automation savings.
