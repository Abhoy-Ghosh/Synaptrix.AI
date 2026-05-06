from io import BytesIO
from datetime import datetime
import os

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Image
)

from reportlab.lib import colors
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

from reportlab.lib.pagesizes import letter
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.enums import TA_CENTER


# =====================================================
# LOGO PATH
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

logo_path = os.path.join(
    BASE_DIR,
    "..",
    "..",
    "assets",
    "logo.png"
)


# =====================================================
# MAIN PDF BUILDER
# =====================================================

def build_pdf(data):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    # =====================================================
    # STYLES
    # =====================================================

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=30,
        leading=36,
        textColor=colors.HexColor('#2563eb'),
        alignment=TA_CENTER,
        spaceAfter=18,
    )

    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['BodyText'],
        fontSize=12,
        leading=18,
        textColor=colors.HexColor('#64748b'),
        alignment=TA_CENTER,
        spaceAfter=22,
    )

    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Heading2'],
        fontSize=18,
        leading=24,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=24,
        spaceAfter=14,
    )

    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['BodyText'],
        fontSize=11,
        leading=18,
        textColor=colors.HexColor('#334155'),
    )

    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['BodyText'],
        fontSize=9,
        leading=14,
        textColor=colors.HexColor('#94a3b8'),
        alignment=TA_CENTER,
    )

    story = []

    # =====================================================
    # LOGO
    # =====================================================

    if os.path.exists(logo_path):

        logo = Image(
            logo_path,
            width=80,
            height=80
        )

        logo.hAlign = 'CENTER'

        story.append(logo)

        story.append(Spacer(1, 16))

    # =====================================================
    # HEADER
    # =====================================================

    story.append(
        Paragraph(
            "<b>Synaptrix AI</b>",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Adaptive Multi-Agent Research Intelligence Report",
            subtitle_style
        )
    )

    generated_time = datetime.now().strftime(
        "%d %B %Y • %H:%M"
    )

    story.append(
        Paragraph(
            f"Generated on {generated_time}",
            subtitle_style
        )
    )

    story.append(Spacer(1, 12))

    topic = data.get(
        "topic",
        "Unknown Topic"
    )

    story.append(
        Paragraph(
            f"<b>Research Topic:</b> {topic}",
            body_style
        )
    )

    story.append(Spacer(1, 18))

    story.append(
        HRFlowable(
            width="100%",
            color=colors.HexColor('#cbd5e1')
        )
    )

    story.append(Spacer(1, 10))

    # =====================================================
    # AGENT OUTPUTS
    # =====================================================

    sections = [

        (
            "Research Summary",
            data.get("summary")
        ),

        (
            "Research Analysis",
            data.get("analysis")
        ),

        (
            "Research Gaps",
            data.get("gaps")
        ),

        (
            "Cross-Paper Synthesis",
            data.get("synthesis")
        ),
    ]

    for title, content in sections:

        story.append(
            Paragraph(
                title,
                section_style
            )
        )

        cleaned = (
            (content or "Not available")
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\n", "<br/>")
        )

        story.append(
            Paragraph(
                cleaned,
                body_style
            )
        )

        story.append(
            Spacer(1, 22)
        )

    # =====================================================
    # PAPER SECTION
    # =====================================================

    papers = data.get(
        "top_papers",
        []
    )

    if papers:

        story.append(PageBreak())

        story.append(
            Paragraph(
                "Top Research Papers",
                section_style
            )
        )

        for idx, paper in enumerate(
            papers,
            start=1
        ):

            title = paper.get(
                "title",
                "Untitled"
            )

            abstract = paper.get(
                "abstract",
                "No abstract"
            )

            authors = ", ".join(
                paper.get(
                    "authors",
                    []
                )
            )

            year = paper.get(
                "year",
                "Unknown"
            )

            story.append(
                Paragraph(
                    f"<b>{idx}. {title}</b>",
                    body_style
                )
            )

            story.append(
                Spacer(1, 4)
            )

            story.append(
                Paragraph(
                    f"<b>Authors:</b> {authors}",
                    body_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Year:</b> {year}",
                    body_style
                )
            )

            story.append(
                Spacer(1, 6)
            )

            story.append(
                Paragraph(
                    abstract,
                    body_style
                )
            )

            story.append(
                Spacer(1, 24)
            )

    # =====================================================
    # FOOTER
    # =====================================================

    story.append(
        Spacer(1, 32)
    )

    story.append(
        HRFlowable(
            width="100%",
            color=colors.HexColor('#cbd5e1')
        )
    )

    story.append(
        Spacer(1, 12)
    )

    story.append(
        Paragraph(
            "Generated by Synaptrix AI — Multi-Agent Research Intelligence Platform",
            footer_style
        )
    )

    # =====================================================
    # BUILD PDF
    # =====================================================

    doc.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf