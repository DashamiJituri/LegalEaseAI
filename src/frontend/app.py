# src/frontend/app.py
import sys, os
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

import parser, summarizer, risk_analyzer, qna_bot, eli5_rewriter, report_generator


st.set_page_config(page_title="LegalEaseAI", layout="wide")
st.title("⚖️ LegalEaseAI — Simplify Complex Legal Documents")
st.subheader("AI-powered tool to summarize, analyze risks, rewrite clauses, and answer questions")


# File upload or manual text input
uploaded_file = st.file_uploader("📂 Upload a legal document (PDF)", type="pdf")
manual_text = st.text_area("📝 Or paste your legal text here:")

if st.button("✨ Simplify Document"):
    if uploaded_file:
        text_to_process = parser.parse_pdf(uploaded_file)
    else:
        text_to_process = manual_text

    if not text_to_process.strip():
        st.warning("⚠️ Please upload a PDF or paste legal text.")
    else:
        st.success("✅ Document processed successfully!")

        # --- Summary ---
        st.subheader("📌 Simplified Summary")
        summary = summarizer.summarize_text(text_to_process)
        st.write(summary)

        # --- Risks ---
        st.subheader("🛡️ Risky Clauses Detected")
        risks = risk_analyzer.analyze_risks(text_to_process)
        risky_count = len([r for r in risks if "⚠️" in r])
        safe_count = max(1, len(text_to_process.split(".")) - risky_count)
        risk_score = max(0, 100 - risky_count * 15)

        st.metric("Contract Safety Score", f"{risk_score} / 100")
        for risk in risks:
            st.warning(risk)

        # --- ELI5 Clause Rewriter ---
        st.subheader("🧑‍🏫 Explain Like I’m 5 (Clause Rewriter)")
        clause_input = st.text_area("Paste a clause for ELI5 rewrite:")
        if st.button("Rewrite Clause"):
            if clause_input:
                rewritten = eli5_rewriter.rewrite_clause(clause_input)
                st.info(f"👉 {rewritten}")

        # --- Visualization ---
        st.subheader("📊 Risk Analysis Visualization")
        fig, ax = plt.subplots()
        ax.pie([risky_count, safe_count], labels=["Risky", "Safe"], autopct="%1.1f%%", startangle=90, colors=["red", "green"])
        ax.axis("equal")
        st.pyplot(fig)

        st.subheader("☁️ Word Cloud of Legal Terms")
        wc = WordCloud(width=800, height=400, background_color="white").generate(text_to_process)
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ax2.imshow(wc, interpolation="bilinear")
        ax2.axis("off")
        st.pyplot(fig2)

        # --- QnA ---
        st.subheader("🤔 Ask your legal document a question")
        question = st.text_input("Enter your question:")
        if question:
            answer = qna_bot.answer_question(text_to_process, question)
            st.info(answer)

        # --- PDF Export ---
        st.subheader("📥 Export Report")
        if st.button("Download PDF Report"):
            output_file = "LegalEaseAI_Report.pdf"
            result = report_generator.generate_report(output_file, summary, risks, risk_score)
            if result is True:
                with open(output_file, "rb") as f:
                    st.download_button("📥 Download Now", f, file_name=output_file, mime="application/pdf")
            else:
                st.error(result)
