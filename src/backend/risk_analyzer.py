# src/backend/risk_analyzer.py
import streamlit as st
from transformers import pipeline

RISK_KEYWORDS = ["penalty", "termination", "liability", "breach", "indemnify", "damages"]

@st.cache_resource
def load_classifier():
    return pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

classifier = load_classifier()

def analyze_risks(text):
    """Detect risky clauses using keyword + sentiment."""
    if not text.strip():
        return ["⚠️ No text provided for risk analysis."]

    risks_found = []
    try:
        # Keyword scan
        for word in RISK_KEYWORDS:
            if word.lower() in text.lower():
                risks_found.append(f"⚠️ Risk keyword detected: **{word}**")

        # Sentiment proxy
        result = classifier(text[:512])
        risks_found.append(f"Sentiment: {result[0]['label']} (score {result[0]['score']:.2f})")

        return risks_found if risks_found else ["✅ No risky clauses detected."]
    except Exception as e:
        return [f"❌ Risk analysis failed: {str(e)}"]
