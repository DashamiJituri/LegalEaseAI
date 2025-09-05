# src/backend/report_generator.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_report(filename, summary, risks, risk_score):
    """
    Generate a PDF report with summary, risks, and score.
    """
    try:
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4

        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "⚖️ LegalEaseAI Report")

        # Metadata
        c.setFont("Helvetica", 10)
        c.drawString(50, height - 70, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Safety Score
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, height - 100, f"Contract Safety Score: {risk_score}/100")

        # Summary
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, height - 140, "Simplified Summary:")
        text_obj = c.beginText(50, height - 160)
        text_obj.setFont("Helvetica", 10)
        for line in summary.split(". "):
            text_obj.textLine(line.strip())
        c.drawText(text_obj)

        # Risks
        y = height - 300
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Risky Clauses:")
        y -= 20
        c.setFont("Helvetica", 10)
        for r in risks:
            c.drawString(60, y, f"- {r}")
            y -= 15

        c.showPage()
        c.save()
        return True
    except Exception as e:
        return f"❌ Report generation failed: {str(e)}"
