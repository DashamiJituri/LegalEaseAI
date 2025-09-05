# src/backend/parser.py
import fitz  # PyMuPDF

def parse_pdf(file):
    """Extracts text from uploaded PDF file."""
    text = ""
    try:
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text("text")
    except Exception as e:
        return f"❌ PDF parsing failed: {str(e)}"
    return text.strip()
