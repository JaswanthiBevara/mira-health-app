"""
ml_model.py — MIRA Custom ML Model
RandomForestClassifier on synthetic clinical data.

Persistence strategy:
- First startup → trains model, saves to mira_model.pkl
- Subsequent startups → loads from mira_model.pkl (< 0.1s)
- Delete mira_model.pkl manually if you want to force retrain
"""

import os
import numpy as np
import joblib

MODEL_PATH = "mira_model.pkl"

# ── Lazy-loaded singleton ─────────────────────────────────────────────────────
_model = None


def _generate_synthetic_data(n_samples: int = 15000):
    """
    Generate synthetic patient data with realistic clinical distributions.
    Groups overlap intentionally to avoid overfitting.
    """
    rng = np.random.default_rng(seed=42)

    n_low    = int(n_samples * 0.40)
    n_medium = int(n_samples * 0.35)
    n_high   = n_samples - n_low - n_medium

    def jitter(arr, scale):
        return arr + rng.normal(0, scale, size=len(arr))

    # ── LOW risk ─────────────────────────────────────────────────────────────
    g_low  = jitter(rng.normal(82,  12,  n_low), 3)
    h_low  = jitter(rng.normal(14.0, 1.5, n_low), 0.3)
    c_low  = jitter(rng.normal(168,  22,  n_low), 5)

    # ── MEDIUM risk ──────────────────────────────────────────────────────────
    g_med  = jitter(rng.normal(115,  18,  n_medium), 4)
    h_med  = jitter(rng.normal(11.0,  1.2, n_medium), 0.3)
    c_med  = jitter(rng.normal(220,   25,  n_medium), 5)

    # ── HIGH risk ────────────────────────────────────────────────────────────
    g_high = jitter(rng.normal(230,  60,  n_high), 6)
    h_high = jitter(rng.normal(7.5,   1.5, n_high), 0.4)
    c_high = jitter(rng.normal(275,   35,  n_high), 6)

    glucose     = np.clip(np.concatenate([g_low, g_med, g_high]), 40, 500)
    haemoglobin = np.clip(np.concatenate([h_low, h_med, h_high]), 3,  20)
    cholesterol = np.clip(np.concatenate([c_low, c_med, c_high]), 80, 450)

    X = np.column_stack([glucose, haemoglobin, cholesterol])
    y = np.array(["Low"] * n_low + ["Medium"] * n_medium + ["High"] * n_high)

    # shuffle
    idx = rng.permutation(len(y))
    return X[idx], y[idx]


def _train_and_save() -> object:
    """Train the model and persist it to disk."""
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import cross_val_score

    print("🤖 MIRA ML: No saved model found. Generating synthetic dataset...")
    X, y = _generate_synthetic_data(n_samples=15000)

    print("🤖 MIRA ML: Training RandomForestClassifier...")
    clf = RandomForestClassifier(
        n_estimators=150,
        max_depth=6,
        min_samples_leaf=20,
        random_state=42,
        n_jobs=-1,
    )
    clf.fit(X, y)

    train_acc = clf.score(X, y) * 100
    cv_scores = cross_val_score(clf, X, y, cv=5, scoring="accuracy")
    cv_acc    = cv_scores.mean() * 100
    gap       = abs(train_acc - cv_acc)
    fit_tag   = "✅ Good fit" if gap < 3 else ("⚠️ Slight overfit" if gap < 8 else "❌ Overfit")

    print(f"🤖 MIRA ML: Training accuracy    : {train_acc:.1f}%")
    print(f"🤖 MIRA ML: CV accuracy (5-fold) : {cv_acc:.1f}%")
    print(f"🤖 MIRA ML: Train-CV gap         : {gap:.1f}% → {fit_tag}")

    joblib.dump(clf, MODEL_PATH)
    print(f"🤖 MIRA ML: Model saved → {MODEL_PATH}")

    return clf


def _load_or_train() -> object:
    """Load model from disk if available, otherwise train and save."""
    if os.path.exists(MODEL_PATH):
        print(f"🤖 MIRA ML: Loading saved model from {MODEL_PATH}...")
        clf = joblib.load(MODEL_PATH)
        print("🤖 MIRA ML: Model loaded ✅ (skipping training)")
        return clf
    return _train_and_save()


def train_model():
    """
    Called once at FastAPI startup.
    Loads from disk if model exists, trains and saves if not.
    """
    global _model
    _model = _load_or_train()


def predict_risk(glucose: float, haemoglobin: float, cholesterol: float) -> tuple[str, float]:
    """
    Returns (risk_label, confidence_pct).
    risk_label: 'Low' | 'Medium' | 'High'
    confidence_pct: 0–100
    """
    global _model
    if _model is None:
        _model = _load_or_train()

    X = np.array([[glucose, haemoglobin, cholesterol]])
    label      = _model.predict(X)[0]
    proba      = _model.predict_proba(X)[0]
    confidence = round(float(proba.max()) * 100, 1)
    return label, confidence


def save_dataset_to_csv(path: str = "mira_synthetic_dataset.csv"):
    """
    Generates the synthetic dataset and saves it as CSV for inspection.
    Run once from terminal:
        python -c "from backend.ml_model import save_dataset_to_csv; save_dataset_to_csv()"
    """
    import pandas as pd
    X, y = _generate_synthetic_data(n_samples=15000)
    df = pd.DataFrame({
        "glucose":     X[:, 0].round(1),
        "haemoglobin": X[:, 1].round(1),
        "cholesterol": X[:, 2].round(1),
        "risk_label":  y,
    })
    df.to_csv(path, index_label="patient_id")
    print(f"Dataset saved to {path} — {len(df)} rows")
    print(df["risk_label"].value_counts())
    return df