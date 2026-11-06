import json
import os
import re
from xml.sax.saxutils import escape
from PIL import Image as PILImage
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "questions.json")
OUTPUT_PDF = os.path.join(BASE_DIR, "mad1_questions_categorized.pdf")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "IIT Madras - Modern Application Development 1 (MAD 1) | Past Year Question Bank")
            self.setStrokeColor(colors.HexColor("#dddddd"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)
            
        # Footer
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, footer_text)
        self.drawString(54, 36, "Confidential - For Personal Educational & Exam Preparation Use")
        self.setStrokeColor(colors.HexColor("#dddddd"))
        self.setLineWidth(0.5)
        self.line(54, 46, 558, 46)
        self.restoreState()

def build_pdf():
    print(f"Loading questions from: {DATA_FILE}")
    if not os.path.exists(DATA_FILE):
        print("Data file not found. Ensure extraction finishes first.")
        return
        
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        questions = json.load(f)
        
    print(f"Total questions to compile: {len(questions)}")
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0f172a'),
        alignment=1, # Center
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#475569'),
        alignment=1,
        spaceAfter=15
    )
    
    week_header_style = ParagraphStyle(
        'WeekHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        textColor=colors.white,
        spaceAfter=0
    )
    
    subtopic_header_style = ParagraphStyle(
        'SubtopicHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=10,
        spaceAfter=6
    )
    
    q_header_style = ParagraphStyle(
        'QHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor('#1e3a8a')
    )
    
    q_stem_style = ParagraphStyle(
        'QStem',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor('#212121'),
        spaceAfter=4
    )
    
    meta_style = ParagraphStyle(
        'MetaText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#64748b'),
        spaceAfter=4
    )
    
    ans_style = ParagraphStyle(
        'AnsText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#15803d'),
        spaceBefore=3,
        spaceAfter=3
    )

    story = []
    
    # Title Page Header
    story.append(Spacer(1, 10))
    story.append(Paragraph("INDIAN INSTITUTE OF TECHNOLOGY MADRAS", ParagraphStyle(
        'InstTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=14,
        textColor=colors.HexColor('#64748b'),
        alignment=1,
        spaceAfter=4
    )))
    story.append(Paragraph("MODERN APPLICATION DEVELOPMENT 1 (MAD 1 / APPDEV 1)", title_style))
    story.append(Paragraph("Comprehensive Past Year CBT Examination Question Bank (301 Authentic Questions)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1e3a8a'), spaceAfter=15))
    
    # Table of Syllabus Statistics
    week_stats = {}
    for q in questions:
        w = q["week"].split(":")[0].strip()
        week_stats[w] = week_stats.get(w, 0) + 1
        
    summary_data = [
        [Paragraph("<b>Curriculum Week</b>", styles['Normal']), Paragraph("<b>Topic Description</b>", styles['Normal']), Paragraph("<b>Questions</b>", styles['Normal'])],
        ["Week 1", "Internet Architecture, HTTP & Network Calculations", f"{week_stats.get('Week 1', 0)} Qs"],
        ["Week 2", "HTML5, CSS3, Box Model & Form Controls", f"{week_stats.get('Week 2', 0)} Qs"],
        ["Week 3", "Backend Python, Flask Essentials, Routing & Request Handling", f"{week_stats.get('Week 3', 0)} Qs"],
        ["Week 4", "Jinja2 Templating, Dynamic Rendering, SQLite & CRUD Applications", f"{week_stats.get('Week 4', 0)} Qs"],
        ["Total", "Verified Authentic Past Exam Questions Across All 4 Weeks", f"{len(questions)} Questions"]
    ]
    t = Table(summary_data, colWidths=[65, 345, 94])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#1e293b')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('LINEBELOW', (0,-1), (-1,-1), 1.5, colors.HexColor('#1e3a8a')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#f8fafc')),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))
    
    # Group questions by Week and Subtopic
    grouped = {}
    for q in questions:
        w = q["week"]
        st = q["subtopic"]
        if w not in grouped:
            grouped[w] = {}
        if st not in grouped[w]:
            grouped[w][st] = []
        grouped[w][st].append(q)
        
    week_order = sorted(grouped.keys())
    
    for week_idx, w in enumerate(week_order):
        if week_idx > 0:
            story.append(PageBreak())
            
        # Week Header Banner Table
        banner = Table([[Paragraph(f"&nbsp;{w.upper()}", week_header_style)]], colWidths=[504])
        banner.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1e3a8a')),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(banner)
        story.append(Spacer(1, 10))
        
        for st in sorted(grouped[w].keys()):
            st_questions = grouped[w][st]
            story.append(Paragraph(f"• {st} ({len(st_questions)} Questions)", subtopic_header_style))
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#94a3b8'), spaceAfter=8))
            
            for q in st_questions:
                q_elements = []
                
                # Question Title & Marks
                q_id = q["id"]
                raw_id = q["raw_q_id"]
                q_type = q["question_type"]
                marks = q["marks"]
                sources = ", ".join(q.get("source_papers", [q.get("paper", "")])[:2])
                
                header_text = f"<b>{q_id}</b> | Type: <b>{q_type}</b> | Marks: <b>+{marks}</b>"
                q_elements.append(Paragraph(header_text, q_header_style))
                q_elements.append(Paragraph(f"Source Exam(s): <i>{escape(sources)}</i>", meta_style))
                
                # Card Image
                card_rel = q.get("card_image", "")
                if card_rel:
                    card_abs = os.path.join(BASE_DIR, card_rel.replace("/", os.sep))
                    if os.path.exists(card_abs):
                        try:
                            with PILImage.open(card_abs) as pil_img:
                                orig_w, orig_h = pil_img.size
                                max_w = 490
                                max_h = 320
                                scale = min(max_w / orig_w, max_h / orig_h, 0.45)
                                target_w = orig_w * scale
                                target_h = orig_h * scale
                                
                            q_elements.append(Spacer(1, 2))
                            q_elements.append(Image(card_abs, width=target_w, height=target_h))
                            q_elements.append(Spacer(1, 2))
                        except Exception as e:
                            pass
                            
                # Official Answer Key
                ans = q.get("correct_answer", [])
                if ans:
                    ans_str = ", ".join(str(a) for a in ans)
                    q_elements.append(Paragraph(f"Official Answer Key: {escape(ans_str)}", ans_style))
                else:
                    q_elements.append(Paragraph("Official Answer Key: [See Official Exam Key / Solutions]", ans_style))
                    
                q_elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e2e8f0'), spaceAfter=8))
                story.append(KeepTogether(q_elements))
                
    print("Building PDF document with NumberedCanvas...")
    doc.build(story, canvasmaker=NumberedCanvas)
    pdf_size_mb = os.path.getsize(OUTPUT_PDF) / (1024 * 1024)
    print(f"Successfully generated: {OUTPUT_PDF} ({pdf_size_mb:.2f} MB)")

if __name__ == "__main__":
    build_pdf()
