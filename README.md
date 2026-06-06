# 🏥 MIRA — Medical Intelligence Robotic Automation

A health prediction app that collects patient blood test results and generates AI-powered health insights.

**Built with:** Python · FastAPI · SQLite · Streamlit · Groq AI (LLaMA 3.3 70B)

---

## 📁 Project Structure

```
mira/
├── backend/
│   ├── database.py       # Database connection
│   ├── models.py         # Patient data model
│   ├── schemas.py        # Input validation
│   ├── ml_model.py       # ML risk prediction
│   ├── ai_service.py     # Groq AI integration
│   └── main.py           # API routes
├── frontend/
│   └── app.py            # Streamlit UI
├── .env.example          # Environment variable template
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/JaswanthiBevara/mira-health-app.git
cd mira-health-app
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
```

Add your Groq API key to the `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

> Get a free Groq API key at https://console.groq.com

### 5. Run the backend

```bash
uvicorn backend.main:app --reload --port 8000
```

The API will be available at **http://localhost:8000**
Interactive API docs at **http://localhost:8000/docs**

### 6. Run the frontend

Open a second terminal and run:

```bash
streamlit run frontend/app.py
```

The app will open at **http://localhost:8501**

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/patients` | Add a new patient |
| GET | `/patients` | View all patients |
| GET | `/patients/{id}` | View one patient |
| PUT | `/patients/{id}` | Update a patient |
| DELETE | `/patients/{id}` | Delete a patient |

---

## 🤖 How AI Works

When a patient record is created or updated, MIRA:

1. Runs blood values through a **RandomForest ML model** to predict risk level (Low / Medium / High)
2. Sends the result to **Groq AI (LLaMA 3.3 70B)** to generate a personalised 2–3 sentence health assessment
3. Stores the combined result in the patient's `remarks` field

---

## ✅ Features

- Add, view, edit, and delete patient records
- Validates email format, date of birth, and blood test values
- Detects duplicate patient entries
- AI-generated health risk assessment for every patient
- Simple and clean Streamlit interface
- Data stored locally using SQLite — no database setup needed

---

## 🔒 Security

- API keys are stored in `.env` and never committed to GitHub
- `.env` is excluded via `.gitignore`

---

*Built for MIRA — Medical Intelligence Robotic Automation*