# src/backend/qna_bot.py
import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_qna():
    return pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

qna = load_qna()

def answer_question(context, question):
    """Answer questions from the document context."""
    if not context.strip():
        return "⚠️ No context available."
    try:
        result = qna(question=question, context=context)
        return result["answer"]
    except Exception as e:
        return f"❌ QnA failed: {str(e)}"
