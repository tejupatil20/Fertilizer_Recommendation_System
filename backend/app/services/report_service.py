"""
ReportLab PDF report generation service.
Generates a professional, letterhead-style PDF for fertilizer recommendations.
"""
import io
from datetime import datetime
from typing import Optional, List

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# Brand colors
GREEN_DARK = colors.HexColor('#15803d')
GREEN_LIGHT = colors.HexColor('#dcfce7')
GREEN_MID = colors.HexColor('#4ade80')
GRAY_LIGHT = colors.HexColor('#f9fafb')
GRAY_MID = colors.HexColor('#e5e7eb')
GRAY_DARK = colors.HexColor('#374151')
WHITE = colors.white


def generate_prediction_report(
    prediction,
    user,
    growth_stages: list,
    knowledge_base_entry=None,
) -> bytes:
    """
    Generate a PDF report for a fertilizer prediction.

    Args:
        prediction: PredictionHistory ORM object
        user: User ORM object
        growth_stages: List of CropGrowthStage ORM objects for the crop
        knowledge_base_entry: Optional FertilizerKnowledgeBase ORM object

    Returns:
        PDF as bytes
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()
    story = []

    # -----------------------------------------------------------------------
    # 1. HEADER BANNER
    # -----------------------------------------------------------------------
    header_data = [
        [Paragraph(
            '<font color="white" size="18"><b>🌱 Smart Fertilizer Recommendation System</b></font>',
            ParagraphStyle('header', fontSize=18, textColor=WHITE, alignment=TA_CENTER),
        )],
        [Paragraph(
            '<font color="white" size="10">AI-Powered Agricultural Advisory Report</font>',
            ParagraphStyle('subheader', fontSize=10, textColor=WHITE, alignment=TA_CENTER),
        )],
    ]
    header_table = Table(header_data, colWidths=[7 * inch])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), GREEN_DARK),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 20),
        ('RIGHTPADDING', (0, 0), (-1, -1), 20),
        ('ROUNDEDCORNERS', [8]),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.2 * inch))

    # -----------------------------------------------------------------------
    # 2. REPORT INFO
    # -----------------------------------------------------------------------
    now_str = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    report_date = prediction.created_at.strftime("%B %d, %Y") if prediction.created_at else now_str

    info_data = [
        ['Report ID:', f'#{prediction.id}', 'Generated:', now_str],
        ['Farmer:', user.username.title(), 'Analysis Date:', report_date],
        ['Role:', user.role.title(), '', ''],
    ]
    info_table = Table(info_data, colWidths=[1.2 * inch, 2.3 * inch, 1.2 * inch, 2.3 * inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), GRAY_LIGHT),
        ('BACKGROUND', (2, 0), (2, -1), GRAY_LIGHT),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY_MID),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.2 * inch))

    # -----------------------------------------------------------------------
    # 3. INPUT PARAMETERS
    # -----------------------------------------------------------------------
    story.append(Paragraph('<b>Input Parameters</b>', ParagraphStyle(
        'section_title', fontSize=12, textColor=GREEN_DARK, spaceAfter=6,
    )))
    story.append(HRFlowable(width="100%", thickness=1.5, color=GREEN_DARK))
    story.append(Spacer(1, 0.1 * inch))

    params_data = [
        ['Parameter', 'Value', 'Parameter', 'Value'],
        ['Crop Type', prediction.crop.title(), 'Days Since Planting', f'{prediction.days_since_planting} days'],
        ['Soil Nitrogen (N)', f'{prediction.soil_n} kg/ha', 'Soil pH', str(prediction.ph)],
        ['Soil Phosphorous (P)', f'{prediction.soil_p} kg/ha', 'Temperature', f'{prediction.temperature}°C'],
        ['Soil Potassium (K)', f'{prediction.soil_k} kg/ha', 'Humidity', f'{prediction.humidity}%'],
        ['Growth Stage', prediction.growth_stage or 'N/A', 'Rainfall', f'{prediction.rainfall} mm'],
    ]
    params_table = Table(params_data, colWidths=[1.8 * inch, 1.7 * inch, 1.8 * inch, 1.7 * inch])
    params_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), GREEN_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 1), (2, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, -1), GRAY_LIGHT),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, GRAY_LIGHT]),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY_MID),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('ALIGN', (3, 0), (3, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(params_table)
    story.append(Spacer(1, 0.2 * inch))

    # -----------------------------------------------------------------------
    # 4. RECOMMENDATION BOX
    # -----------------------------------------------------------------------
    story.append(Paragraph('<b>Fertilizer Recommendation</b>', ParagraphStyle(
        'section_title', fontSize=12, textColor=GREEN_DARK, spaceAfter=6,
    )))
    story.append(HRFlowable(width="100%", thickness=1.5, color=GREEN_DARK))
    story.append(Spacer(1, 0.1 * inch))

    confidence_pct = round(prediction.confidence_score, 1)
    dosage_str = f"{prediction.dosage_kg_per_acre} kg/acre" if prediction.dosage_kg_per_acre else "See notes below"

    rec_data = [
        ['🌿 Recommended Fertilizer', '📊 Confidence Score', '⚖️ Dosage', '🌱 Growth Stage'],
        [
            Paragraph(f'<b><font size="14">{prediction.predicted_fertilizer}</font></b>',
                      ParagraphStyle('rec', alignment=TA_CENTER)),
            Paragraph(f'<b><font size="14">{confidence_pct}%</font></b>',
                      ParagraphStyle('conf', alignment=TA_CENTER)),
            Paragraph(f'<b>{dosage_str}</b>',
                      ParagraphStyle('dos', alignment=TA_CENTER)),
            Paragraph(f'<b>{prediction.growth_stage or "N/A"}</b>',
                      ParagraphStyle('gs', alignment=TA_CENTER)),
        ],
    ]
    rec_table = Table(rec_data, colWidths=[1.75 * inch, 1.75 * inch, 1.75 * inch, 1.75 * inch])
    rec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), GREEN_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BACKGROUND', (0, 1), (0, 1), GREEN_LIGHT),
        ('BACKGROUND', (1, 1), (1, 1), GRAY_LIGHT),
        ('BACKGROUND', (2, 1), (2, 1), GREEN_LIGHT),
        ('BACKGROUND', (3, 1), (3, 1), GRAY_LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.5, GREEN_MID),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(rec_table)
    story.append(Spacer(1, 0.15 * inch))

    # -----------------------------------------------------------------------
    # 5. GEMINI EXPLANATION
    # -----------------------------------------------------------------------
    if prediction.gemini_explanation:
        explanation_data = [
            [Paragraph('<b>🤖 AI Explanation (Gemini)</b>',
                       ParagraphStyle('ai_title', fontSize=10, textColor=GREEN_DARK))],
            [Paragraph(prediction.gemini_explanation,
                       ParagraphStyle('ai_body', fontSize=9, leading=14, textColor=GRAY_DARK))],
        ]
        if prediction.application_method:
            explanation_data.append([Paragraph(
                f'<b>Application Method:</b> {prediction.application_method}',
                ParagraphStyle('method', fontSize=9, textColor=GRAY_DARK),
            )])
        if prediction.timing_advice:
            explanation_data.append([Paragraph(
                f'<b>Timing Advice:</b> {prediction.timing_advice}',
                ParagraphStyle('timing', fontSize=9, textColor=GRAY_DARK),
            )])

        exp_table = Table(explanation_data, colWidths=[7 * inch])
        exp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), GREEN_LIGHT),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BOX', (0, 0), (-1, -1), 1, GREEN_DARK),
            ('LINEBELOW', (0, 0), (-1, 0), 1, GREEN_MID),
        ]))
        story.append(exp_table)
        story.append(Spacer(1, 0.2 * inch))

    # -----------------------------------------------------------------------
    # 6. CROP APPLICATION CALENDAR
    # -----------------------------------------------------------------------
    if growth_stages:
        story.append(Paragraph('<b>Crop Application Calendar — Full Cycle</b>', ParagraphStyle(
            'section_title', fontSize=12, textColor=GREEN_DARK, spaceAfter=6,
        )))
        story.append(HRFlowable(width="100%", thickness=1.5, color=GREEN_DARK))
        story.append(Spacer(1, 0.1 * inch))

        cal_header = ['Stage Name', 'Days Range', 'Recommended Fertilizer', 'Dose %', 'Notes']
        cal_data = [cal_header]
        for stage in growth_stages:
            cal_data.append([
                stage.stage_name,
                f'{stage.min_days}–{stage.max_days}',
                stage.recommended_fertilizer or '—',
                f'{stage.dose_percentage}%' if stage.dose_percentage else '—',
                Paragraph(stage.notes or '', ParagraphStyle('note', fontSize=7, leading=10)),
            ])

        cal_table = Table(
            cal_data,
            colWidths=[1.6 * inch, 0.9 * inch, 1.4 * inch, 0.6 * inch, 2.5 * inch],
        )
        cal_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), GREEN_DARK),
            ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, GREEN_LIGHT]),
            ('GRID', (0, 0), (-1, -1), 0.5, GRAY_MID),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('ALIGN', (3, 0), (3, -1), 'CENTER'),
        ]))
        story.append(cal_table)
        story.append(Spacer(1, 0.2 * inch))

    # -----------------------------------------------------------------------
    # 7. PRECAUTIONS
    # -----------------------------------------------------------------------
    if knowledge_base_entry and knowledge_base_entry.precautions:
        prec_data = [
            [Paragraph('<b>⚠️ Precautions & Best Practices</b>',
                       ParagraphStyle('prec_title', fontSize=10, textColor=colors.HexColor('#92400e')))],
            [Paragraph(knowledge_base_entry.precautions,
                       ParagraphStyle('prec_body', fontSize=9, leading=14, textColor=GRAY_DARK))],
        ]
        if knowledge_base_entry.composition:
            prec_data.insert(1, [Paragraph(
                f'<b>Composition:</b> {knowledge_base_entry.composition}',
                ParagraphStyle('comp', fontSize=9, textColor=GRAY_DARK),
            )])

        prec_table = Table(prec_data, colWidths=[7 * inch])
        prec_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fef3c7')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#d97706')),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(prec_table)
        story.append(Spacer(1, 0.2 * inch))

    # -----------------------------------------------------------------------
    # 8. FOOTER
    # -----------------------------------------------------------------------
    footer_data = [
        [
            Paragraph('<font size="8" color="gray">© 2026 Smart Fertilizer Recommendation System | AI-Powered Agricultural Advisory</font>',
                      ParagraphStyle('footer_l', fontSize=8, textColor=colors.gray, alignment=TA_LEFT)),
            Paragraph(f'<font size="8" color="gray">Generated: {now_str}</font>',
                      ParagraphStyle('footer_r', fontSize=8, textColor=colors.gray, alignment=TA_RIGHT)),
        ]
    ]
    footer_table = Table(footer_data, colWidths=[3.5 * inch, 3.5 * inch])
    footer_table.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('LINEABOVE', (0, 0), (-1, 0), 0.5, GRAY_MID),
    ]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GRAY_MID))
    story.append(Spacer(1, 0.05 * inch))
    story.append(Paragraph(
        '<font size="7" color="gray"><i>Disclaimer: This report is generated by an AI system for advisory purposes only. '
        'Consult a certified agronomist before making major fertilizer decisions.</i></font>',
        ParagraphStyle('disclaimer', fontSize=7, textColor=colors.gray, alignment=TA_CENTER),
    ))
    story.append(Spacer(1, 0.05 * inch))
    story.append(footer_table)

    doc.build(story)
    buffer.seek(0)
    return buffer.read()
