"""
ai_service.py
─────────────
Calls Groq API with full patient context including age.
Returns a health prediction stored in the `remarks` field.
Model: llama-3.3-70b-versatile (free tier — 14,400 req/day)
"""

import os
from datetime import date
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are a medical AI assistant. Given a patient's age and blood test values,
provide a brief, clear health risk assessment in 2-3 sentences.
Factor in age-related risks — the same blood values carry different risks 
for a 25-year-old vs a 65-year-old.
Be informative but avoid alarmist language.
Always recommend consulting a doctor for proper diagnosis.
Respond in plain text only — no bullet points, no markdown.
"""


def get_health_prediction(
    full_name:   str,
    dob:         str,
    glucose:     float,
    haemoglobin: float,
    cholesterol: float,
) -> str:
    """
    Sends patient age + blood values to Groq.
    Returns a 2-3 sentence health prediction string.
    """
    # Calculate age from DOB
    birth_date = date.fromisoformat(str(dob))
    age        = (date.today() - birth_date).days // 365

    user_message = f"""
Patient name    : {full_name}
Age             : {age} years
Glucose         : {glucose} mg/dL    (normal fasting: 70–99 mg/dL)
Haemoglobin     : {haemoglobin} g/dL  (normal: 12–17.5 g/dL)
Cholesterol     : {cholesterol} mg/dL (normal: below 200 mg/dL)

Based on this patient's age and blood test values, assess possible 
health risks or conditions. Consider age as a key factor — older 
patients have higher baseline cardiovascular and metabolic risk.
Keep the response to 2-3 sentences. Recommend a doctor consultation.
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
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"AI prediction unavailable: {str(e)}"