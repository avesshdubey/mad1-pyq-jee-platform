import fitz
import os
import re
import json
from PIL import Image

WORKSPACE_DIR = r"C:\Users\avesh\Desktop\mad1-pyq-jee-platform"
DATA_FILE = os.path.join(WORKSPACE_DIR, "data", "questions.json")
PYQS_DIR = r"C:\Users\avesh\Desktop\PYQS"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    questions = json.load(f)

print(f"Total questions to re-crop and sanitize: {len(questions)}")

paper_paths = {}
for root, dirs, files in os.walk(PYQS_DIR):
    for f in files:
        if f.lower().endswith(".pdf"):
            paper_paths[f] = os.path.join(root, f)

labels = ["(A)", "(B)", "(C)", "(D)", "(E)", "(F)"]

def sanitize_page_vector(page, opt_y_start=0):
    # 1. Mask small icon images (checkmarks / red crosses)
    for img in page.get_image_info(xrefs=True):
        if img['width'] <= 30 and img['height'] <= 30:
            r = fitz.Rect(img['bbox'])
            r.x0 -= 5
            r.y0 -= 5
            r.x1 += 5
            r.y1 += 5
            page.draw_rect(r, color=(1, 1, 1), fill=(1, 1, 1))

    # Find Options : section
    opt_heading = page.search_for("Options :")
    if opt_heading:
        opt_y = opt_heading[0].y0
    else:
        opt_y = opt_y_start

    # 2. Recolor all colored text spans in options area to neutral black
    page_json = json.loads(page.get_text("json"))
    for b in page_json.get("blocks", []):
        for l in b.get("lines", []):
            for s in l.get("spans", []):
                txt = s.get("text", "").strip()
                bbox = fitz.Rect(s["bbox"])
                if bbox.y0 >= opt_y - 8:
                    c = s.get("color", 0)
                    r = (c >> 16) & 255
                    g = (c >> 8) & 255
                    b_col = c & 255
                    is_colored = (g > r + 30 and g > b_col + 30) or (r > g + 40 and r > b_col + 40)
                    is_opt_num = re.match(r'^\d{10,}\.?$', txt)
                    if is_colored or is_opt_num:
                        page.draw_rect(bbox, color=(1, 1, 1), fill=(1, 1, 1))
                        if not is_opt_num and txt:
                            font_size = s.get("size", 11)
                            page.insert_text(fitz.Point(bbox.x0, bbox.y1 - 1.5), s["text"], fontsize=font_size, color=(0.1, 0.1, 0.1))

    # 3. Mask left gutter option numbers and replace with (A), (B), (C), (D)
    opt_spans = []
    for b in page_json.get("blocks", []):
        for l in b.get("lines", []):
            for s in l.get("spans", []):
                txt = s.get("text", "").strip()
                if re.match(r'^\d{10,}\.?$', txt) and s["bbox"][1] >= opt_y - 8:
                    opt_spans.append(s["bbox"])

    opt_spans.sort(key=lambda b: b[1])
    for idx, bbox in enumerate(opt_spans):
        mask_r = fitz.Rect(20, bbox[1] - 4, 130, bbox[3] + 4)
        page.draw_rect(mask_r, color=(1, 1, 1), fill=(1, 1, 1))
        lbl = labels[idx] if idx < len(labels) else f"({idx+1})"
        page.insert_text(fitz.Point(30, bbox[3] - 2), lbl, fontsize=12, color=(0.15, 0.2, 0.3))

processed_count = 0
cont_count = 0

for q in questions:
    pname = q.get("paper")
    if pname not in paper_paths:
        continue
    raw_id = str(q.get("raw_q_id"))
    pno = q.get("page") - 1
    card_rel = q.get("card_image", "")
    card_path = os.path.join(WORKSPACE_DIR, card_rel.replace("/", os.sep))
    
    doc = fitz.open(paper_paths[pname])
    page0 = doc[pno]
    
    # Locate exact Question Id
    qid_rects = page0.search_for(raw_id)
    if not qid_rects:
        # Check adjacent pages
        if pno > 0 and doc[pno - 1].search_for(raw_id):
            pno -= 1
            page0 = doc[pno]
            qid_rects = page0.search_for(raw_id)
        elif pno + 1 < len(doc) and doc[pno + 1].search_for(raw_id):
            pno += 1
            page0 = doc[pno]
            qid_rects = page0.search_for(raw_id)
            
    if not qid_rects:
        print(f"Error: Could not locate QID {raw_id} in {pname}")
        doc.close()
        continue
        
    qid_r = qid_rects[0]
    
    # Find Question Label strictly belonging to THIS question
    ql_rects = [r for r in page0.search_for("Question Label") if abs(r.y0 - qid_r.y0) < 80 and r.y0 >= qid_r.y0 - 20]
    top_y = (ql_rects[0].y1 + 4) if ql_rects else (qid_r.y1 + 4)
    
    # Find bottom bound on page0: must stop before next question or sub-section
    next_q_rects = [r for r in page0.search_for("Question Number") if r.y0 > top_y + 30]
    sub_rects = [r for r in page0.search_for("Sub-Section Number") if r.y0 > top_y + 30]
    
    cands0 = []
    if next_q_rects: cands0.append(min(r.y0 for r in next_q_rects) - 6)
    if sub_rects: cands0.append(min(r.y0 for r in sub_rects) - 6)
    bot_y = min(cands0) if cands0 else (page0.rect.height - 20)
    
    # Check if question continues onto page1
    txt0 = page0.get_text(clip=fitz.Rect(0, top_y, page0.rect.width, bot_y))
    opt_ids = [str(o.get('option_id')) for o in q.get('options', [])]
    found_opts = [oid for oid in opt_ids if oid in txt0]
    has_continuation = (("Options :" not in txt0) or (len(opt_ids) > 0 and len(found_opts) < len(opt_ids))) and (pno + 1 < len(doc))
    
    # Sanitize page 0
    sanitize_page_vector(page0, opt_y_start=top_y)
    
    rect0 = fitz.Rect(20, max(0, top_y), page0.rect.width - 20, min(page0.rect.height, bot_y))
    pix0 = page0.get_pixmap(clip=rect0, dpi=150)
    img0 = Image.frombytes("RGB", [pix0.width, pix0.height], pix0.samples)
    
    if has_continuation:
        cont_count += 1
        page1 = doc[pno + 1]
        
        # Find where continuation ends on page 1
        next_q1 = [r for r in page1.search_for("Question Number") if r.y0 > 50]
        sub_q1 = [r for r in page1.search_for("Sub-Section Number") if r.y0 > 50]
        cands1 = []
        if next_q1: cands1.append(min(r.y0 for r in next_q1) - 6)
        if sub_q1: cands1.append(min(r.y0 for r in sub_q1) - 6)
        bot_y1 = min(cands1) if cands1 else (page1.rect.height - 20)
        
        # Sanitize page 1
        sanitize_page_vector(page1, opt_y_start=0)
        
        rect1 = fitz.Rect(20, 20, page1.rect.width - 20, min(page1.rect.height - 20, bot_y1))
        pix1 = page1.get_pixmap(clip=rect1, dpi=150)
        img1 = Image.frombytes("RGB", [pix1.width, pix1.height], pix1.samples)
        
        final_w = max(img0.width, img1.width)
        final_h = img0.height + img1.height
        final_img = Image.new("RGB", (final_w, final_h), (255, 255, 255))
        final_img.paste(img0, (0, 0))
        final_img.paste(img1, (0, img0.height))
    else:
        final_img = img0

    # Resize if oversized
    if final_img.width > 960 and final_img.height > 10:
        target_h = max(50, int(final_img.height * 960 / final_img.width))
        final_img = final_img.resize((960, target_h), Image.Resampling.LANCZOS)
        
    final_img.save(card_path, "JPEG", quality=82, optimize=True)
    processed_count += 1
    doc.close()

print(f"Successfully processed and sanitized {processed_count} cards! Continuations: {cont_count}")
