import fitz
import os
import re
import json
from PIL import Image
import numpy as np

WORKSPACE_DIR = r"C:\Users\avesh\Desktop\mad1-pyq-jee-platform"
DATA_FILE = os.path.join(WORKSPACE_DIR, "data", "questions.json")
PYQS_DIR = r"C:\Users\avesh\Desktop\PYQS"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    questions = json.load(f)

print(f"Total questions to sanitize: {len(questions)}")

paper_paths = {}
for root, dirs, files in os.walk(PYQS_DIR):
    for f in files:
        if f.lower().endswith(".pdf"):
            paper_paths[f] = os.path.join(root, f)

labels = ["(A)", "(B)", "(C)", "(D)", "(E)", "(F)"]

def sanitize_page(page, option_ids):
    # 1. Mask all small checkmark / red cross icon images
    for img in page.get_image_info(xrefs=True):
        if img['width'] <= 28 and img['height'] <= 28:
            r = fitz.Rect(img['bbox'])
            r.x0 -= 5
            r.y0 -= 5
            r.x1 += 5
            r.y1 += 5
            page.draw_rect(r, color=(1, 1, 1), fill=(1, 1, 1))

    # 2. Find option IDs and mask the left gutter (x from 20 to 135)
    page_json = json.loads(page.get_text("json"))
    opt_spans = []
    for b in page_json.get("blocks", []):
        for l in b.get("lines", []):
            for s in l.get("spans", []):
                txt = s.get("text", "").strip()
                if any(txt.startswith(oid) for oid in option_ids) or re.match(r'^\d{10,}\.?$', txt):
                    opt_spans.append(s["bbox"])

    opt_spans.sort(key=lambda b: b[1])
    for idx, bbox in enumerate(opt_spans):
        # Mask left gutter containing colored option number and checkmark/cross
        mask_r = fitz.Rect(20, bbox[1] - 4, 135, bbox[3] + 4)
        page.draw_rect(mask_r, color=(1, 1, 1), fill=(1, 1, 1))
        # Draw clean neutral dark label
        lbl = labels[idx] if idx < len(labels) else f"({idx+1})"
        page.insert_text(fitz.Point(30, bbox[3] - 2), lbl, fontsize=12, color=(0.15, 0.2, 0.3))

def sweep_pixel_spoils(pil_img):
    # Secondary defense: sweep left column for any remaining green or red tick pixels
    arr = np.array(pil_img)
    h, w = arr.shape[:2]
    left_limit = min(220, w)
    
    # Check green pixels in left gutter
    green_mask = (arr[:, :left_limit, 1].astype(int) - arr[:, :left_limit, 0].astype(int) > 35) & \
                 (arr[:, :left_limit, 1].astype(int) - arr[:, :left_limit, 2].astype(int) > 35) & \
                 (arr[:, :left_limit, 1] > 130)
                 
    coords_g = np.argwhere(green_mask)
    if len(coords_g) > 0:
        for y, x in coords_g:
            # Paint white box around it
            y0 = max(0, y - 8)
            y1 = min(h, y + 8)
            x0 = max(0, x - 8)
            x1 = min(left_limit, x + 8)
            arr[y0:y1, x0:x1] = [255, 255, 255]
            
    # Check red cross pixels in left gutter
    red_mask = (arr[:, :left_limit, 0].astype(int) - arr[:, :left_limit, 1].astype(int) > 50) & \
               (arr[:, :left_limit, 0].astype(int) - arr[:, :left_limit, 2].astype(int) > 50) & \
               (arr[:, :left_limit, 0] > 160)
               
    coords_r = np.argwhere(red_mask)
    if len(coords_r) > 0:
        for y, x in coords_r:
            y0 = max(0, y - 8)
            y1 = min(h, y + 8)
            x0 = max(0, x - 8)
            x1 = min(left_limit, x + 8)
            arr[y0:y1, x0:x1] = [255, 255, 255]

    return Image.fromarray(arr)

sanitized_count = 0

for q in questions:
    pname = q.get("paper")
    if pname not in paper_paths:
        continue
    raw_id = q.get("raw_q_id")
    pno = q.get("page") - 1
    card_rel = q.get("card_image", "")
    card_path = os.path.join(WORKSPACE_DIR, card_rel.replace("/", os.sep))
    option_ids = [o["option_id"] for o in q.get("options", [])]
    
    doc = fitz.open(paper_paths[pname])
    page0 = doc[pno]
    
    # Check if question spans onto next page
    text0 = page0.get_text()
    m_this = re.search(r'Question Id\s*:\s*' + re.escape(raw_id), text0)
    has_continuation = False
    page1 = None
    if m_this and pno + 1 < len(doc) and "Options :" not in text0[m_this.start():]:
        has_continuation = True
        page1 = doc[pno + 1]

    # Sanitize page 0
    sanitize_page(page0, option_ids)
    if has_continuation and page1:
        sanitize_page(page1, option_ids)

    # Calculate crop bounds for page 0
    # Omit administrative metadata: crop starts below Question Label
    ql_rects = page0.search_for("Question Label")
    if not ql_rects:
        ql_rects = page0.search_for(f"Question Id : {raw_id}")
    top_y = ql_rects[0].y1 + 4 if ql_rects else 20
    
    if has_continuation and page1:
        # Page 0 goes to bottom
        rect0 = fitz.Rect(20, max(0, top_y), page0.rect.width - 20, page0.rect.height - 20)
        pix0 = page0.get_pixmap(clip=rect0, dpi=150)
        img0 = Image.frombytes("RGB", [pix0.width, pix0.height], pix0.samples)
        
        # Page 1 goes up to next question or section
        text1 = page1.get_text()
        m_next_q = re.search(r'Question Number\s*:\s*\d+', text1)
        y_next_end = 400
        if m_next_q:
            sr1 = page1.search_for(m_next_q.group(0))
            if sr1:
                y_next_end = sr1[0].y0 - 10
        rect1 = fitz.Rect(20, 20, page1.rect.width - 20, min(page1.rect.height - 20, max(60, y_next_end)))
        pix1 = page1.get_pixmap(clip=rect1, dpi=150)
        img1 = Image.frombytes("RGB", [pix1.width, pix1.height], pix1.samples)
        
        total_w = max(img0.width, img1.width)
        total_h = img0.height + img1.height
        final_img = Image.new("RGB", (total_w, total_h), (255, 255, 255))
        final_img.paste(img0, (0, 0))
        final_img.paste(img1, (0, img0.height))
    else:
        # Single page crop
        bot_rects = page0.search_for("Sub-Section Number")
        if not bot_rects:
            bot_rects = page0.search_for("Question Number")
            bot_rects = [r for r in bot_rects if r.y0 > top_y + 60]
        bot_y = bot_rects[0].y0 - 5 if bot_rects else page0.rect.height - 20
        
        if bot_y <= top_y + 40:
            bot_y = page0.rect.height - 20
        if top_y >= bot_y - 40:
            top_y = 20
        
        clip_r = fitz.Rect(20, max(0, top_y), page0.rect.width - 20, min(page0.rect.height, bot_y))
        pix = page0.get_pixmap(clip=clip_r, dpi=150)
        final_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Secondary pixel-level defense to ensure zero checkmarks
    final_img = sweep_pixel_spoils(final_img)
    
    # Resize if oversized
    if final_img.width > 960 and final_img.height > 10:
        target_h = max(50, int(final_img.height * 960 / final_img.width))
        final_img = final_img.resize((960, target_h), Image.Resampling.LANCZOS)

    final_img.save(card_path, "JPEG", quality=82, optimize=True)
    sanitized_count += 1
    doc.close()

print(f"Successfully sanitized and saved all {sanitized_count} question cards without green ticks or red crosses!")
