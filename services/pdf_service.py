from fpdf import FPDF
import tempfile
import os

def generate_pdf_report(metadata: dict, filename=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Agri Optimization Report", ln=True)
    pdf.ln(4)
    for k,v in metadata.items():
        pdf.multi_cell(0, 8, f"{k}: {v}")
    if not filename:
        fd, filename = tempfile.mkstemp(suffix=".pdf")
        os.close(fd)
    pdf.output(filename)
    return filename
