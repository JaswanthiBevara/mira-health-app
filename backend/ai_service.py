"""
ai_service.py
─────────────
Combines ML risk prediction with Groq AI text explanation.

Flow:
  1. ml_model.predict_risk()  → (label, confidence) tuple
  2. Groq LLaMA 3.3 70B       → personalised text explanation
  3. Combined result stored in remarks field
"""

import os
from datetime import date
from groq import Groq
from dotenv import load_dotenv
from backend.ml_model import predict_risk

load_dotenv()

_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are a medical AI assistant. You will be given a patient's blood test 
values along with a machine learning risk score. Write a 2-3 sentence 
personalised health assessment that:
1. Acknowledges the ML risk level
2. Explains which specific values are concerning and why
3. Gives one actionable recommendation
Be medically informative, clear, and always recommend consulting a doctor.
Respond in plain text only — no bullet points, no markdown, no headers.
"""


def _risk_emoji(label: str) -> str:
    return {"Low": "🟢", "Medium": "🟡", "High": "🔴"}.get(label, "⚪")


def get_health_prediction(
    full_name:   str,
    dob:         str,
    glucose:     float,
    haemoglobin: float,
    cholesterol: float,
) -> str:
    """
    Step 1: ML model predicts risk level + confidence
    Step 2: Groq generates personalised explanation
    Step 3: Combined remarks string returned
    """

    # ── Step 1: ML prediction ─────────────────────────────────────────────────
    label, confidence = predict_risk(glucose, haemoglobin, cholesterol)
    emoji = _risk_emoji(label)

    # ── Step 2: Calculate age ─────────────────────────────────────────────────
    birth_date = date.fromisoformat(str(dob))
    age        = (date.today() - birth_date).days // 365

    # ── Step 3: Groq explanation ──────────────────────────────────────────────
    user_message = f"""
Patient      : {full_name}, Age {age} years
Glucose      : {glucose} mg/dL   (normal: 70–99)
Haemoglobin  : {haemoglobin} g/dL (normal: 12–17.5)
Cholesterol  : {cholesterol} mg/dL (normal: <200)

ML Risk Score: {label} ({confidence}% confidence)

Write a 2-3 sentence personalised health assessment for this patient.
"""

    try:
        response = _client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_message},
            ],
            temperature=0.4,
            max_tokens=200,
        )
        ai_text = response.choices[0].message.content.strip()

    except Exception as e:
        ai_text = f"AI assessment unavailable: {str(e)}"

    # ── Step 4: Format combined remarks ──────────────────────────────────────
    remarks = (
    f"{emoji} ML Risk Prediction: {label.upper()}\n\n"
    f"{ai_text}"
)

    return remarks