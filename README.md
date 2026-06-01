# 🏥 MIRA — Medical Intelligence Robotic Automation

A health prediction application that collects patient blood test results and generates AI-powered health insights using **Groq AI (LLaMA 3.3 70B)**.

Built with: **Python · FastAPI · MySQL · SQLAlchemy · Streamlit · Groq API**

---

## 📁 Project Structure

```
mira/
├── backend/
│   ├── __init__.py       # Package init
│   ├── database.py       # MySQL connection (SQLAlchemy)
│   ├── models.py         # ORM model → patients table
│   ├── schemas.py        # Pydantic validation schemas
│   ├── ai_service.py     # Groq API integration
│   └── main.py           # FastAPI routes (CRUD)
├── frontend/
│   └── app.py            # Streamlit UI
├── .env.example          # Environment variable template
├── .env                  # ← YOU CREATE THIS (never commit)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/mira-health-app.git
cd mira-health-app
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up MySQL database

Open MySQL and run:

```sql
CREATE DATABASE mira_db;
CREATE USER 'mira_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON mira_db.* TO 'mira_user'@'localhost';
FLUSH PRIVILEGES;
```

### 5. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` with your actual values:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=mira_db
DB_USER=mira_user
DB_PASSWORD=your_mysql_password

GROQ_API_KEY=your_groq_api_key
```

> Get a **free Groq API key** at https://console.groq.com

### 6. Run the backend (FastAPI)

```bash
uvicorn backend.main:app --reload --port 8000
```

- API runs at: http://localhost:8000
- Interactive API docs: http://localhost:8000/docs

### 7. Run the frontend (Streamlit)

Open a **second terminal** (with venv activated):

```bash
streamlit run frontend/app.py
```

- UI runs at: http://localhost:8501

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/patients` | Create patient + AI prediction |
| GET | `/patients` | List all patients |
| GET | `/patients/{id}` | Get single patient |
| PUT | `/patients/{id}` | Update patient + refresh AI |
| DELETE | `/patients/{id}` | Delete patient |

Full interactive docs available at `/docs` when backend is running.

---

## 🤖 AI Prediction

When a patient record is created or updated, the app sends blood test values to the **Groq API** (LLaMA 3.3 70B model) and receives a 2–3 sentence health risk assessment stored in the `remarks` field.

- **Free tier**: 14,400 requests/day
- **Speed**: Sub-second inference
- **Model**: `llama-3.3-70b-versatile`

---

## 🗃️ Database Schema

```sql
CREATE TABLE patients (
    id           INT PRIMARY KEY AUTO_INCREMENT,
    full_name    VARCHAR(150) NOT NULL,
    dob          DATE NOT NULL,
    email        VARCHAR(200) NOT NULL UNIQUE,
    glucose      FLOAT NOT NULL,
    haemoglobin  FLOAT NOT NULL,
    cholesterol  FLOAT NOT NULL,
    remarks      TEXT
);
```

> SQLAlchemy auto-creates this table on first run.

---

## ✅ Features

- Full CRUD operations for patient records
- Input validation (email format, DOB not in future, numeric blood values)
- AI-generated health prediction on every create/update
- Clean Streamlit UI with tab navigation
- MySQL persistent storage
- Environment-based configuration (no hardcoded credentials)

---

## 🔒 Security Notes

- All credentials stored in `.env` (excluded from git via `.gitignore`)
- Never commit your `.env` file
- Only `.env.example` with placeholder values is committed

---

*Built for MIRA — Medical Intelligence Robotic Automation*
