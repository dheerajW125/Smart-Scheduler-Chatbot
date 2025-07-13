# 🧠 Smart Scheduler – AI-powered Calendar Assistant

Smart Scheduler is an intelligent chatbot-powered scheduling assistant built with **FastAPI**, **Google Calendar API**, and **NLP**. It lets users schedule, view, and delete calendar events using natural language like:

> “Fix a meeting with Elsa tomorrow at 10 am”  
> “List all upcoming meetings”  
> “Cancel my 3pm call with Alex”

---

## 🚀 Features

✅ Chat-based interaction via API  
✅ NLP-powered intent detection (create/list/delete)  
✅ Google Calendar integration (OAuth2)  
✅ Supports natural phrases like “tomorrow 3pm” using `dateparser`  
✅ Modular and extensible codebase (services, schema, etc.)

---

## 🛠 Tech Stack

- **Python 3.10+**
- **FastAPI**
- **Google Calendar API (via `google-api-python-client`)**
- **spaCy** (`en_core_web_sm`)
- **dateparser** – for flexible date/time parsing

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/smart-scheduler.git
cd smart-scheduler

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
python -m spacy download en_core_web_sm

### 2. Setup Google Calendar API Credentials
Go to Google Cloud Console

Create a new project

Enable Google Calendar API

Go to OAuth consent screen → choose External and add scopes:

https://www.googleapis.com/auth/calendar

Download your credentials.json file and place it in the project root

###3. F First Run (OAuth Consent Flow)
  python main.py - This will open a browser window asking you to authenticate with your Google account. On success, it saves a token.json file locally.

Run the Server
uvicorn main:app --reload
Visit the interactive docs at:
➡️ http://127.0.0.1:8000/docs


API Usage
POST /chat
Request
{
  "message": "schedule a meeting with John next Friday at 2pm"
}
Response

{
  "message": "✅ Event created: schedule a meeting with John next Friday at 2pm"
}

📁 Project Structure
smart-scheduler/
│
├── app/
│   ├── calendar.py         # Google Calendar logic
│   ├── nlp.py              # NLPService using spaCy + dateparser
│   ├── schema.py           # Pydantic schema for API request
│
├── main.py                 # FastAPI entrypoint
├── credentials.json        # Your OAuth2 credentials (ignored by .gitignore)
├── token.json              # Token generated after user consent
├── requirements.txt
└── README.md

🧠 Example Queries
"Schedule a call with Priya at 4pm tomorrow"
"Book a meeting on next Monday at 9am"
"Show my meetings"
"Cancel my lunch with Raj"

📌 TODO / Improvements
✅ Add duration parsing (e.g., “for 30 minutes”)
🌐 Add timezone support
🧑‍💼 Add multiple user OAuth support
💬 Optional chatbot UI with React / Telegram Bot

📄 License
MIT License.
Feel free to use and extend this project!

Built with ❤️ by Dheeraj Warkar
