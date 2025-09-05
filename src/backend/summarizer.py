# src/backend/summarizer.py
import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

summarizer = load_summarizer()

def summarize_text(text):
    """Summarize legal text into plain English."""
    if not text.strip():
        return "⚠️ No text provided."
    try:
        result = summarizer(text, max_length=120, min_length=30, do_sample=False)
        return result[0]["summary_text"]
    except Exception as e:
        return f"❌ Summarization failed: {str(e)}"
