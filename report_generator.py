# report_generator.py

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import time
import os


def generate_pdf(results):
    """Generate a clean, simple PDF summarizing the analysis."""

    filename = f"opportunity_report_{int(time.time())}.pdf"
    filepath = os.path.join(filename)

    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "Molecule Repurposing Opportunity Report")

    # Molecule
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 90, f"Molecule: {results['molecule']}")

    # Summary Section
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 130, "Executive Summary:")

    text = c.beginText(50, height - 150)
    text.setFont("Helvetica", 11)
    text.setLeading(14)

    summary_lines = split_text(results["summary"], 90)
    for line in summary_lines:
        text.textLine(line)

    c.drawText(text)

    # END PAGE 1
    c.showPage()

    # ------------------------------
    # PAGE 2 : MARKET & TRIALS
    # ------------------------------
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 50, "Market Insights")
    text = c.beginText(50, height - 80)
    text.setFont("Helvetica", 11)
    text.setLeading(14)

    for k, v in results["market"].items():
        text.textLine(f"{k}: {v}")

    c.drawText(text)
    c.showPage()

    # ------------------------------
    # PAGE 3 : PATENTS & WEB
    # ------------------------------
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 50, "Patent Landscape")
    text = c.beginText(50, height - 80)
    text.setFont("Helvetica", 11)
    text.setLeading(14)

    for p in results["patents"]:
        text.textLine(f"{p}")

    c.drawText(text)
    c.showPage()

    # End file
    c.save()
    return filepath


def split_text(text, max_chars):
    """Helper utility to split long text into lines for PDF."""
    words = text.split()
    lines = []
    current = ""

    for w in words:
        if len(current) + len(w) + 1 <= max_chars:
            current += " " + w if current else w
        else:
            lines.append(current)
            current = w

    if current:
        lines.append(current)

    return lines
