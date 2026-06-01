"""
app.py — MIRA Frontend (Light Premium UI + Dynamic Remarks)
────────────────────────────────────────────────────────
Streamlit UI for the MIRA Health Prediction Application.
Design: Clinical premium — light surfaces, teal accents, minimal gradients.
Features: CRUD, Search, Delete Confirm, Blood Indicators,
          Dynamic Remarks Color, CSV Export, Pagination

Run with:
    streamlit run frontend/app.py
"""

import re
import io
import csv
import requests
import streamlit as st
from datetime import date, datetime


# ── Config ────────────────────────────────────────────────────────────────────
API_BASE = "https://mira-health-app-0h7b.onrender.com"
PAGE_SIZE = 10

st.set_page_config(
    page_title="MIRA — Health Prediction",
    page_icon="🏥",
    layout="wide",
)


# ── Premium Light CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg: #f4f7fb;
    --surface: #ffffff;
    --surface-2: #f8fbfd;
    --surface-3: #eef4f8;
    --surface-soft: #f5f8fc;

    --border: rgba(15, 23, 42, 0.08);
    --border-strong: rgba(20, 184, 166, 0.20);

    --text: #102033;
    --text-muted: #5f738c;
    --text-soft: #7b8ca3;
    --text-faint: #94a3b8;

    --accent: #0f9f94;
    --accent-2: #14b8a6;
    --accent-soft: rgba(20, 184, 166, 0.10);

    --input-bg: #ffffff;
    --input-border: #d9e3ec;
    --input-text: #0f172a;
    --input-placeholder: #94a3b8;

    --success: #10b981;
    --success-bg: rgba(16, 185, 129, 0.08);
    --warning: #f59e0b;
    --warning-bg: rgba(245, 158, 11, 0.10);
    --danger: #ef4444;
    --danger-bg: rgba(239, 68, 68, 0.08);
    --info: #0ea5e9;
    --info-bg: rgba(14, 165, 233, 0.08);

    --shadow-sm: 0 8px 24px rgba(15, 23, 42, 0.06);
    --shadow-md: 0 14px 36px rgba(15, 23, 42, 0.10);

    --radius-sm: 10px;
    --radius-md: 14px;
    --radius-lg: 18px;
}

*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
}

section[data-testid="stSidebar"] {
    background: var(--surface) !important;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding: 2rem 2.4rem 1.2rem !important;
    max-width: 1240px !important;
}

/* Header */
.mira-header {
    display: flex;
    align-items: center;
    gap: 1.2rem;
    padding: 1.4rem 1.6rem;
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid var(--border);
    border-radius: 22px;
    margin-bottom: 2rem;
    box-shadow: var(--shadow-sm);
}
.mira-logo {
    width: 60px;
    height: 60px;
    background: linear-gradient(180deg, #24c7b7 0%, #13a79b 100%);
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.65rem;
    flex-shrink: 0;
    box-shadow: 0 10px 24px rgba(20, 184, 166, 0.18);
}
.mira-title {
    font-family: 'DM Serif Display', serif !important;
    font-size: 2.2rem !important;
    color: #0f2137 !important;
    margin: 0 !important;
    line-height: 1.05 !important;
    letter-spacing: -0.4px;
}
.mira-subtitle {
    font-size: 0.92rem !important;
    color: var(--text-muted) !important;
    margin: 0.25rem 0 0 !important;
    font-weight: 400 !important;
    letter-spacing: 0.2px;
}
.mira-badge {
    margin-left: auto;
    background: var(--accent-soft);
    border: 1px solid rgba(20, 184, 166, 0.24);
    color: var(--accent);
    padding: 0.45rem 0.95rem;
    border-radius: 999px;
    font-size: 0.76rem;
    font-weight: 700;
    letter-spacing: 0.9px;
    text-transform: uppercase;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface-2) !important;
    border-radius: 14px !important;
    padding: 4px !important;
    gap: 6px !important;
    border: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-soft) !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.7rem 1.35rem !important;
    transition: all 0.2s ease !important;
}
.stTabs [aria-selected="true"] {
    background: #ffffff !important;
    color: var(--accent) !important;
    border: 1px solid rgba(20, 184, 166, 0.18) !important;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04) !important;
}
.stTabs [data-baseweb="tab-border"] {
    display: none !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 1.35rem !important;
}

/* Cards */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.5rem 1.7rem;
    margin-bottom: 1.1rem;
    box-shadow: var(--shadow-sm);
}
.card-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.12rem;
    color: var(--text);
    margin: 0 0 0.28rem;
}
.card-sub {
    font-size: 0.86rem;
    color: var(--text-muted);
    margin: 0;
}
.section-label {
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 1.3px;
    text-transform: uppercase;
    color: var(--accent);
    margin: 1.4rem 0 0.8rem;
}

/* Inputs */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stDateInput > div > div > input,
.stDateInput > div > div,
[data-baseweb="input"] input,
[data-baseweb="base-input"] input {
    background: var(--input-bg) !important;
    border: 1px solid var(--input-border) !important;
    border-radius: 12px !important;
    color: var(--input-text) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.92rem !important;
    padding: 0.68rem 0.95rem !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stDateInput > div > div > input:focus {
    border-color: #5eead4 !important;
    box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.16) !important;
    background: #ffffff !important;
}
.stTextInput label,
.stNumberInput label,
.stDateInput label,
.stSelectbox label {
    color: var(--text-muted) !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.2px !important;
}
.stTextInput > div > div > input::placeholder,
.stNumberInput > div > div > input::placeholder {
    color: var(--input-placeholder) !important;
}
.stNumberInput > div > div > button {
    background: #f4f8fb !important;
    border: 1px solid #d9e3ec !important;
    color: #0f172a !important;
}
.stNumberInput > div > div > button:hover {
    background: #e8fbf8 !important;
    border-color: #8de8de !important;
    color: #0f172a !important;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button,
.stDownloadButton > button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    transition: all 0.18s ease !important;
    font-size: 0.88rem !important;
    min-height: 42px !important;
}
.stButton > button[kind="primary"],
.stFormSubmitButton > button {
    background: linear-gradient(180deg, #24c7b7 0%, #13a79b 100%) !important;
    border: 1px solid rgba(20, 184, 166, 0.18) !important;
    color: white !important;
    box-shadow: 0 8px 18px rgba(20, 184, 166, 0.18) !important;
}
.stButton > button[kind="primary"]:hover,
.stFormSubmitButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 12px 24px rgba(20, 184, 166, 0.22) !important;
}
.stButton > button[kind="secondary"] {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-muted) !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: rgba(20, 184, 166, 0.24) !important;
    color: var(--accent) !important;
    background: #ffffff !important;
}
.stDownloadButton > button {
    background: var(--surface-2) !important;
    border: 1px solid rgba(20, 184, 166, 0.18) !important;
    color: var(--accent) !important;
}
.stDownloadButton > button:hover {
    background: #ffffff !important;
    border-color: rgba(20, 184, 166, 0.28) !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.91rem !important;
    padding: 1rem 1.15rem !important;
}
.streamlit-expanderHeader:hover {
    background: var(--surface-2) !important;
    border-color: rgba(20, 184, 166, 0.18) !important;
}
.streamlit-expanderContent {
    background: var(--surface-soft) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 14px 14px !important;
    padding: 1.15rem 1.35rem !important;
}

/* Metrics */
[data-testid="metric-container"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 1.15rem 1.3rem !important;
    box-shadow: var(--shadow-sm);
}
[data-testid="metric-container"] label {
    color: var(--text-soft) !important;
    font-size: 0.76rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.6px !important;
    text-transform: uppercase !important;
}
[data-testid="metric-container"] [data-testid="metric-value"] {
    color: var(--text) !important;
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.75rem !important;
}

/* Alerts */
.stSuccess {
    background: var(--success-bg) !important;
    border: 1px solid rgba(16, 185, 129, 0.22) !important;
    border-radius: 12px !important;
    color: #047857 !important;
}
.stError {
    background: var(--danger-bg) !important;
    border: 1px solid rgba(239, 68, 68, 0.18) !important;
    border-radius: 12px !important;
    color: #b91c1c !important;
}
.stWarning {
    background: var(--warning-bg) !important;
    border: 1px solid rgba(245, 158, 11, 0.20) !important;
    border-radius: 12px !important;
    color: #b45309 !important;
}
.stInfo {
    background: var(--info-bg) !important;
    border: 1px solid rgba(14, 165, 233, 0.18) !important;
    border-radius: 12px !important;
    color: #0369a1 !important;
}

/* Custom components */
.remarks-box {
    border-radius: 12px;
    padding: 1rem 1.2rem;
    font-size: 0.92rem;
    line-height: 1.75;
    margin-top: 0.8rem;
    border: 1px solid transparent;
}
.validation-box {
    background: rgba(239, 68, 68, 0.06);
    border: 1px solid rgba(239, 68, 68, 0.16);
    border-radius: 10px;
    padding: 0.72rem 0.9rem;
    margin-bottom: 0.45rem;
    font-size: 0.85rem;
    color: #b91c1c;
}
.duplicate-box {
    background: rgba(245, 158, 11, 0.08);
    border: 1px solid rgba(245, 158, 11, 0.18);
    border-radius: 12px;
    padding: 1rem 1.15rem;
    font-size: 0.9rem;
    color: #9a3412;
    margin-top: 0.85rem;
}
.confirm-box {
    background: rgba(245, 158, 11, 0.08);
    border: 1px solid rgba(245, 158, 11, 0.18);
    border-radius: 12px;
    padding: 0.9rem 1.05rem;
    margin-top: 0.7rem;
    font-size: 0.88rem;
    color: #9a3412;
}
.patient-field-label {
    font-size: 0.74rem;
    color: var(--text-soft);
    font-weight: 700;
    letter-spacing: 0.45px;
    text-transform: uppercase;
    margin-bottom: 0.12rem;
}
.patient-field-value {
    font-size: 0.93rem;
    color: var(--text);
    font-weight: 400;
    margin-bottom: 0.8rem;
}
.blood-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.55rem;
    flex-wrap: wrap;
}
.blood-value {
    font-size: 1rem;
    font-weight: 700;
    color: var(--text);
}
.blood-unit {
    font-size: 0.78rem;
    color: var(--text-soft);
}
.badge-normal,
.badge-warning,
.badge-danger {
    padding: 3px 9px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 700;
    border: 1px solid transparent;
}
.badge-normal {
    background: rgba(16, 185, 129, 0.10);
    color: #047857;
    border-color: rgba(16, 185, 129, 0.16);
}
.badge-warning {
    background: rgba(245, 158, 11, 0.12);
    color: #b45309;
    border-color: rgba(245, 158, 11, 0.18);
}
.badge-danger {
    background: rgba(239, 68, 68, 0.10);
    color: #b91c1c;
    border-color: rgba(239, 68, 68, 0.16);
}
.divider {
    border: none;
    border-top: 1px solid rgba(15, 23, 42, 0.08);
    margin: 1rem 0;
}
.search-hint {
    font-size: 0.82rem;
    color: var(--text-soft);
    margin-top: 0.25rem;
}
.page-info {
    text-align: center;
    color: var(--text-soft);
    font-size: 0.85rem;
    padding-top: 0.55rem;
}
.footer {
    text-align: center;
    color: #7b8ca3;
    font-size: 0.78rem;
    padding: 1.4rem 0 0.4rem;
    letter-spacing: 0.2px;
}
.range-hint {
    font-size: 0.76rem;
    color: #7b8ca3;
    margin-top: 0.25rem;
    margin-bottom: 0.5rem;
    line-height: 1.5;
}
.range-normal { color: #047857; }
.range-warning { color: #b45309; }
.range-danger { color: #b91c1c; }

::-webkit-scrollbar { width: 7px; }
::-webkit-scrollbar-track { background: #eef3f8; }
::-webkit-scrollbar-thumb { background: #c7d4e0; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #8fcfc7; }

@media (max-width: 900px) {
    .block-container {
        padding: 1.2rem 1rem 1rem !important;
    }
    .mira-header {
        padding: 1.2rem 1rem;
        border-radius: 18px;
        align-items: flex-start;
        flex-wrap: wrap;
    }
    .mira-title {
        font-size: 1.8rem !important;
    }
    .mira-badge {
        margin-left: 0;
    }
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def blood_indicator(value, low_ok, high_ok, high_warn):
    if low_ok <= value <= high_ok:
        return "🟢", "Normal", "badge-normal"
    elif value <= high_warn or value < low_ok:
        return "🟡", "Borderline", "badge-warning"
    else:
        return "🔴", "High Risk", "badge-danger"


def glucose_indicator(v):
    return blood_indicator(v, 70, 99, 125)


def haemoglobin_indicator(v):
    return blood_indicator(v, 12, 17.5, 11)


def cholesterol_indicator(v):
    return blood_indicator(v, 0, 200, 239)


def get_remarks_style(glucose, haemoglobin, cholesterol):
    g_e = glucose_indicator(glucose)[0]
    h_e = haemoglobin_indicator(haemoglobin)[0]
    c_e = cholesterol_indicator(cholesterol)[0]
    indicators = [g_e, h_e, c_e]

    if "🔴" in indicators:
        return (
            "background: rgba(254, 226, 226, 0.85);"
            "border: 1px solid rgba(239, 68, 68, 0.18);"
            "color: #b91c1c;"
        )
    elif "🟡" in indicators:
        return (
            "background: rgba(255, 247, 237, 0.92);"
            "border: 1px solid rgba(245, 158, 11, 0.18);"
            "color: #9a3412;"
        )
    else:
        return (
            "background: rgba(236, 253, 245, 0.95);"
            "border: 1px solid rgba(16, 185, 129, 0.16);"
            "color: #047857;"
        )


def is_valid_email(email: str):
    pattern = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email.strip().lower()):
        return False, "Email format is invalid. Example: name@gmail.com"
    tld = email.split(".")[-1]
    if any(c.isdigit() for c in tld):
        return False, f"'.{tld}' is not a valid email extension."
    return True, ""


def validate_patient_inputs(full_name, email, dob, glucose, haemoglobin, cholesterol):
    errors = []

    if not full_name.strip():
        errors.append("Full name is required.")
    elif len(full_name.strip()) < 2:
        errors.append("Full name must be at least 2 characters.")
    elif re.search(r'\\d', full_name):
        errors.append("Full name should not contain numbers.")

    if not email.strip():
        errors.append("Email address is required.")
    else:
        valid, reason = is_valid_email(email)
        if not valid:
            errors.append(reason)

    if dob >= date.today():
        errors.append("Date of birth must be a past date.")
    else:
        age = (date.today() - dob).days // 365
        if age > 150:
            errors.append("Date of birth is too far in the past.")
        elif age < 1:
            errors.append("Patient must be at least 1 year old.")

    if glucose <= 0:
        errors.append("Glucose must be a positive number.")
    elif glucose > 1000:
        errors.append(f"Glucose {glucose} mg/dL exceeds max (1000).")

    if haemoglobin <= 0:
        errors.append("Haemoglobin must be a positive number.")
    elif haemoglobin > 25:
        errors.append(f"Haemoglobin {haemoglobin} g/dL exceeds max (25).")

    if cholesterol <= 0:
        errors.append("Cholesterol must be a positive number.")
    elif cholesterol > 1000:
        errors.append(f"Cholesterol {cholesterol} mg/dL exceeds max (1000).")

    return errors


# ── API ───────────────────────────────────────────────────────────────────────
def api_get_all():
    try:
        r = requests.get(f"{API_BASE}/patients", timeout=10)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to backend. Make sure FastAPI is running on port 8000."
    except Exception as e:
        return None, str(e)


def api_create(payload):
    try:
        r = requests.post(f"{API_BASE}/patients", json=payload, timeout=20)
        if r.status_code == 201:
            return r.json(), None, None
        detail = r.json().get("detail", "Unknown error.")
        if r.status_code == 409:
            return None, None, detail
        return None, detail, None
    except Exception as e:
        return None, str(e), None


def api_update(patient_id, payload):
    try:
        r = requests.put(f"{API_BASE}/patients/{patient_id}", json=payload, timeout=20)
        if r.status_code == 200:
            return r.json(), None, None
        detail = r.json().get("detail", "Unknown error.")
        if r.status_code == 409:
            return None, None, detail
        return None, detail, None
    except Exception as e:
        return None, str(e), None


def api_delete(patient_id):
    try:
        r = requests.delete(f"{API_BASE}/patients/{patient_id}", timeout=10)
        if r.status_code == 200:
            return True, None
        return False, r.json().get("detail", "Unknown error.")
    except Exception as e:
        return False, str(e)


def build_csv(patients):
    output = io.StringIO()
    fields = ["id", "full_name", "dob", "email", "glucose", "haemoglobin", "cholesterol", "remarks"]
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    for p in patients:
        writer.writerow({k: p.get(k, "") for k in fields})
    return output.getvalue().encode("utf-8")


# ── Patient form ──────────────────────────────────────────────────────────────
def patient_form(prefix: str, defaults: dict = None):
    d = defaults or {}
    payload = None

    with st.form(key=f"form_{prefix}"):
        st.markdown('<p class="section-label">👤 Patient Information</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            full_name = st.text_input(
                "Full Name *",
                value=d.get("full_name", ""),
                placeholder="e.g. Ravi Kumar",
            )
            email = st.text_input(
                "Email Address *",
                value=d.get("email", ""),
                placeholder="e.g. ravi@gmail.com",
            )

        with col2:
            default_dob = d.get("dob", None)
            if isinstance(default_dob, str):
                default_dob = datetime.strptime(default_dob, "%Y-%m-%d").date()

            dob = st.date_input(
                "Date of Birth *",
                value=default_dob or date(1990, 1, 1),
                min_value=date(1900, 1, 1),
                max_value=date.today(),
                help="Patient's date of birth — must be a past date",
            )

        st.markdown('<p class="section-label">🩸 Blood Test Values</p>', unsafe_allow_html=True)
        col3, col4, col5 = st.columns(3)

        with col3:
            glucose = st.number_input(
                "Glucose (mg/dL) *",
                min_value=0.0,
                max_value=1000.0,
                value=float(d.get("glucose", 0.0)) if d.get("glucose") else 0.0,
                step=0.1,
                format="%.1f",
                help="🟢 Normal: 70–99 | 🟡 Prediabetes: 100–125 | 🔴 Diabetes: ≥126",
            )

        with col4:
            haemoglobin = st.number_input(
                "Haemoglobin (g/dL) *",
                min_value=0.0,
                max_value=25.0,
                value=float(d.get("haemoglobin", 0.0)) if d.get("haemoglobin") else 0.0,
                step=0.1,
                format="%.1f",
                help="🟢 Normal: 12–17.5 | 🟡 Mild anaemia: 10–11.9 | 🔴 Severe: <10",
            )

        with col5:
            cholesterol = st.number_input(
                "Cholesterol (mg/dL) *",
                min_value=0.0,
                max_value=1000.0,
                value=float(d.get("cholesterol", 0.0)) if d.get("cholesterol") else 0.0,
                step=0.1,
                format="%.1f",
                help="🟢 Normal: <200 | 🟡 Borderline: 200–239 | 🔴 High: ≥240",
            )

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        submitted = st.form_submit_button(
            "✦ Save & Generate AI Health Prediction",
            use_container_width=True,
            type="primary",
        )

        if submitted:
            errors = validate_patient_inputs(
                full_name, email, dob, glucose, haemoglobin, cholesterol
            )
            if errors:
                st.error(f"Please fix {len(errors)} error(s) before submitting:")
                for err in errors:
                    st.markdown(
                        f"<div class='validation-box'>⚠ {err}</div>",
                        unsafe_allow_html=True,
                    )
            else:
                payload = {
                    "full_name": full_name.strip(),
                    "dob": str(dob),
                    "email": email.strip().lower(),
                    "glucose": round(glucose, 1),
                    "haemoglobin": round(haemoglobin, 1),
                    "cholesterol": round(cholesterol, 1),
                }

    return payload


# ── Session state ─────────────────────────────────────────────────────────────
for key, default in {"edit_patient": None, "refresh": 0, "page": 0}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ══════════════════════════════════════════════════════════════════════════════
# PAGE
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="mira-header">
    <div class="mira-logo">🏥</div>
    <div>
        <p class="mira-title">MIRA</p>
        <p class="mira-subtitle">Medical Intelligence Robotic Automation</p>
    </div>
    <div class="mira-badge">⬤ Live</div>
</div>
""", unsafe_allow_html=True)

tab_add, tab_view = st.tabs(["  ➕  Add Patient  ", "  📋  Patient Records  "])


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — ADD PATIENT
# ─────────────────────────────────────────────────────────────────────────────
with tab_add:
    st.markdown("""
    <div class="card">
        <p class="card-title">Register New Patient</p>
        <p class="card-sub">Complete all fields · AI health prediction is auto-generated on save</p>
    </div>
    """, unsafe_allow_html=True)

    payload = patient_form(prefix="create")

    if payload:
        with st.spinner("Analysing blood values with Groq AI (LLaMA 3.3 70B)..."):
            result, error, duplicate = api_create(payload)

        if duplicate:
            st.markdown(f"""
<div class='duplicate-box'>
⚠ <strong>Patient already registered</strong><br><br>
A record with email <strong>{payload['email']}</strong> already exists.<br>
Switch to <strong>Patient Records</strong> tab to view or edit it.
</div>
""", unsafe_allow_html=True)

        elif error:
            st.error(f"Server error: {error}")

        else:
            st.success(f"✓ {result['full_name']} registered successfully")
            st.markdown("**AI Health Prediction**")
            style = get_remarks_style(
                result["glucose"], result["haemoglobin"], result["cholesterol"]
            )
            st.markdown(
                f"<div class='remarks-box' style='{style}'>{result.get('remarks', 'N/A')}</div>",
                unsafe_allow_html=True,
            )
            st.session_state.refresh += 1


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — ALL PATIENTS
# ─────────────────────────────────────────────────────────────────────────────
with tab_view:
    if st.session_state.edit_patient:
        p = st.session_state.edit_patient
        st.markdown(f"""
        <div class="card">
            <p class="card-title">✏ Editing — {p['full_name']}</p>
            <p class="card-sub">Update values and save · AI prediction refreshes automatically</p>
        </div>
        """, unsafe_allow_html=True)

        updated = patient_form(prefix="edit", defaults=p)

        if updated:
            with st.spinner("Refreshing AI prediction..."):
                result, error, duplicate = api_update(p["id"], updated)

            if duplicate:
                st.markdown(f"""
<div class='duplicate-box'>
⚠ <strong>Email already in use</strong><br>
<strong>{updated['email']}</strong> belongs to another patient.
Please use a different email.
</div>
""", unsafe_allow_html=True)

            elif error:
                st.error(f"Server error: {error}")

            else:
                st.success(f"✓ {result['full_name']} updated successfully")
                st.markdown("**Updated AI Prediction**")
                style = get_remarks_style(
                    result["glucose"], result["haemoglobin"], result["cholesterol"]
                )
                st.markdown(
                    f"<div class='remarks-box' style='{style}'>{result.get('remarks', 'N/A')}</div>",
                    unsafe_allow_html=True,
                )
                st.session_state.edit_patient = None
                st.session_state.refresh += 1
                st.rerun()

        if st.button("← Cancel", type="secondary"):
            st.session_state.edit_patient = None
            st.rerun()

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    ctrl1, ctrl2 = st.columns([4, 1])

    with ctrl1:
        search = st.text_input(
            "search",
            placeholder="🔍 Search by name or email...",
            label_visibility="collapsed",
        )

    with ctrl2:
        if st.button("↺ Refresh", use_container_width=True):
            st.session_state.refresh += 1
            st.session_state.page = 0
            st.rerun()

    with st.spinner("Loading records..."):
        patients, error = api_get_all()

    if error:
        st.error(f"{error}")
        st.info("Start the backend: `uvicorn backend.main:app --reload --port 8000`")

    elif not patients:
        st.info("No patients registered yet. Use Add Patient tab to get started.")

    else:
        if search.strip():
            q = search.strip().lower()
            patients = [
                p for p in patients
                if q in p["full_name"].lower() or q in p["email"].lower()
            ]

        total_filtered = len(patients)
        total_pages = max(1, (total_filtered + PAGE_SIZE - 1) // PAGE_SIZE)

        if st.session_state.page >= total_pages:
            st.session_state.page = 0

        sm1, sm2 = st.columns([4, 2])

        with sm1:
            label = (
                f"Showing {total_filtered} result(s) for '{search}'"
                if search.strip()
                else f"{total_filtered} patient(s) on record"
            )
            st.markdown(f"<p class='search-hint'>{label}</p>", unsafe_allow_html=True)

        with sm2:
            st.download_button(
                "⬇ Export CSV",
                data=build_csv(patients),
                file_name=f"mira_patients_{date.today()}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        start = st.session_state.page * PAGE_SIZE
        page_patients = patients[start:start + PAGE_SIZE]

        for p in page_patients:
            g_e, g_l, g_b = glucose_indicator(p["glucose"])
            h_e, h_l, h_b = haemoglobin_indicator(p["haemoglobin"])
            c_e, c_l, c_b = cholesterol_indicator(p["cholesterol"])

            with st.expander(
                f"  {p['full_name']}   ·   {p['email']}   ·   {g_e}{h_e}{c_e}   ·   ID #{p['id']}",
                expanded=False,
            ):
                col_a, col_b, col_c = st.columns(3)

                with col_a:
                    st.markdown("<p class='patient-field-label'>Full Name</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='patient-field-value'>{p['full_name']}</p>", unsafe_allow_html=True)
                    st.markdown("<p class='patient-field-label'>Date of Birth</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='patient-field-value'>{p['dob']}</p>", unsafe_allow_html=True)
                    st.markdown("<p class='patient-field-label'>Email</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='patient-field-value'>{p['email']}</p>", unsafe_allow_html=True)

                with col_b:
                    st.markdown("<p class='patient-field-label'>Glucose</p>", unsafe_allow_html=True)
                    st.markdown(f"""
<div class='blood-row'>
  <span class='blood-value'>{p['glucose']}</span>
  <span class='blood-unit'>mg/dL</span>
  <span class='{g_b}'>{g_e} {g_l}</span>
</div>""", unsafe_allow_html=True)

                    st.markdown("<p class='patient-field-label'>Haemoglobin</p>", unsafe_allow_html=True)
                    st.markdown(f"""
<div class='blood-row'>
  <span class='blood-value'>{p['haemoglobin']}</span>
  <span class='blood-unit'>g/dL</span>
  <span class='{h_b}'>{h_e} {h_l}</span>
</div>""", unsafe_allow_html=True)

                    st.markdown("<p class='patient-field-label'>Cholesterol</p>", unsafe_allow_html=True)
                    st.markdown(f"""
<div class='blood-row'>
  <span class='blood-value'>{p['cholesterol']}</span>
  <span class='blood-unit'>mg/dL</span>
  <span class='{c_b}'>{c_e} {c_l}</span>
</div>""", unsafe_allow_html=True)

                with col_c:
                    st.markdown("<p class='patient-field-label'>AI Health Prediction</p>", unsafe_allow_html=True)
                    remarks = p.get("remarks") or "No prediction available."
                    style = get_remarks_style(
                        p["glucose"], p["haemoglobin"], p["cholesterol"]
                    )
                    st.markdown(
                        f"<div class='remarks-box' style='margin-top:0; {style}'>{remarks}</div>",
                        unsafe_allow_html=True,
                    )

                st.markdown("<hr class='divider'>", unsafe_allow_html=True)

                b1, b2, _ = st.columns([1, 1, 4])

                with b1:
                    if st.button("✏ Edit", key=f"edit_{p['id']}", use_container_width=True):
                        st.session_state.edit_patient = p
                        st.rerun()

                with b2:
                    if st.button(
                        "🗑 Delete",
                        key=f"del_{p['id']}",
                        use_container_width=True,
                        type="secondary",
                    ):
                        st.session_state[f"confirm_{p['id']}"] = True

                if st.session_state.get(f"confirm_{p['id']}"):
                    st.markdown(f"""
<div class='confirm-box'>
⚠ Are you sure you want to permanently delete
<strong>{p['full_name']}</strong>? This cannot be undone.
</div>
""", unsafe_allow_html=True)

                    y1, y2, _ = st.columns([1, 1, 4])

                    with y1:
                        if st.button(
                            "✓ Confirm Delete",
                            key=f"yes_{p['id']}",
                            use_container_width=True,
                            type="primary",
                        ):
                            ok, err = api_delete(p["id"])
                            if err:
                                st.error(err)
                            else:
                                st.success(f"Deleted: {p['full_name']}")
                                st.session_state.pop(f"confirm_{p['id']}", None)
                                st.session_state.refresh += 1
                                st.rerun()

                    with y2:
                        if st.button("✕ Cancel", key=f"no_{p['id']}", use_container_width=True):
                            st.session_state.pop(f"confirm_{p['id']}", None)
                            st.rerun()

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        pg1, pg2, pg3 = st.columns([1, 3, 1])

        with pg1:
            if st.button(
                "← Prev",
                use_container_width=True,
                disabled=(st.session_state.page == 0),
            ):
                st.session_state.page -= 1
                st.rerun()

        with pg2:
            st.markdown(
                f"<p class='page-info'>Page {st.session_state.page + 1} of "
                f"{total_pages} &nbsp;·&nbsp; {total_filtered} patients</p>",
                unsafe_allow_html=True,
            )

        with pg3:
            if st.button(
                "Next →",
                use_container_width=True,
                disabled=(st.session_state.page >= total_pages - 1),
            ):
                st.session_state.page += 1
                st.rerun()


st.markdown("""
<p class='footer'>
MIRA — Medical Intelligence Robotic Automation &nbsp;·&nbsp;
Groq AI · LLaMA 3.3 70B &nbsp;·&nbsp;
FastAPI · MySQL · Streamlit
</p>
""", unsafe_allow_html=True)