# src/backend/eli5_rewriter.py
import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_rewriter():
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

rewriter = load_rewriter()

def rewrite_clause(clause: str) -> str:
    """Rewrites a clause into plain English (ELI5 mode)."""
    if not clause.strip():
        return "⚠️ No clause provided."
    try:
        result = rewriter(clause, max_length=60, min_length=10, do_sample=False)
        return result[0]["summary_text"]
    except Exception as e:
        return f"❌ ELI5 rewriting failed: {str(e)}"
