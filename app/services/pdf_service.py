import io
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def generate_pdf_report(analysis_data: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.75 * inch)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle", parent=styles["Title"], fontSize=22, spaceAfter=6
    )
    heading_style = ParagraphStyle(
        "HeadingStyle", parent=styles["Heading2"], spaceBefore=16, spaceAfter=8
    )
    body_style = styles["BodyText"]

    elements = []

    elements.append(Paragraph(f"DevInsight AI Report", title_style))
    elements.append(Paragraph(f"{analysis_data['owner']}/{analysis_data['repo']}", styles["Heading3"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"Health Score: {analysis_data['health_score']}/100", heading_style))

    table_data = [["Category", "Score", "Weight", "Contribution"]]
    for category, values in analysis_data["breakdown"].items():
        table_data.append([
            category.replace("_", " ").title(),
            str(values["raw_score"]),
            str(values["weight"]),
            str(values["contribution"]),
        ])

    table = Table(table_data, colWidths=[2 * inch, 1.3 * inch, 1.3 * inch, 1.3 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4f46e5")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(table)

    ai = analysis_data["ai_summary"]
    elements.append(Paragraph("AI Summary", heading_style))
    elements.append(Paragraph(ai["overview"], body_style))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(f"<b>Tech Stack:</b> {ai['tech_stack_explanation']}", body_style))
    elements.append(Paragraph(f"<b>Strongest Area:</b> {ai['strongest_area']}", body_style))
    elements.append(Paragraph(f"<b>Weakest Area:</b> {ai['weakest_area']}", body_style))

    elements.append(Paragraph("Improvement Suggestions", heading_style))
    for suggestion in ai["improvement_suggestions"]:
        elements.append(Paragraph(f"• {suggestion}", body_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()