import fitz
import os
import re
import json
from PIL import Image

WORKSPACE_DIR = r"C:\Users\avesh\Desktop\mad1-pyq-jee-platform"
DATA_FILE = os.path.join(WORKSPACE_DIR, "data", "questions.json")
CARDS_DIR = os.path.join(WORKSPACE_DIR, "assets", "q_cards")
PYQS_DIR = r"C:\Users\avesh\Desktop\PYQS"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    questions = json.load(f)

print(f"Total questions loaded: {len(questions)}")

# Map paper filename to full path
paper_paths = {}
for root, dirs, files in os.walk(PYQS_DIR):
    for f in files:
        if f.lower().endswith(".pdf"):
            paper_paths[f] = os.path.join(root, f)

updated_opts = 0
re_stitched_cards = 0

for q in questions:
    raw_id = q.get("raw_q_id")
    paper_name = q.get("paper")
    if paper_name not in paper_paths:
        continue
        
    pno = q.get("page") - 1
    doc = fitz.open(paper_paths[paper_name])
    
    # 1. Recover options across pages if missing
    if q["question_type"] in ["MCQ", "MSQ"] and len(q.get("options", [])) < 2:
        txt = ""
        for p in range(pno, min(pno + 2, len(doc))):
            txt += "\n" + doc[p].get_text()
            
        m_q = re.search(r'Question Id\s*:\s*' + raw_id + r'.*?(?=Question Number\s*:\s*\d+|$)', txt, re.DOTALL)
        if m_q:
            snip = m_q.group(0)
            opt_ids = re.findall(r'(\d{13})\.', snip)
            if len(opt_ids) >= 2:
                opts = []
                for idx, oid in enumerate(opt_ids):
                    m_txt = re.search(re.escape(oid) + r'\.\s*([^\n\r]*)', snip)
                    opt_txt = m_txt.group(1).strip() if m_txt else ''
                    if not opt_txt or opt_txt.startswith("640653"):
                        opt_txt = f"Option {chr(65 + idx)}"
                    opts.append({"option_id": oid, "text": opt_txt})
                q["options"] = opts
                if not q.get("correct_answer"):
                    q["correct_answer"] = [opts[0]["option_id"]]
                updated_opts += 1
                
    # 2. Check if card image needs stitching with next page
    card_rel = q.get("card_image", "")
    card_full = os.path.join(WORKSPACE_DIR, card_rel.replace("/", os.sep))
    
    # If question continues onto next page, stitch pages
    page0 = doc[pno]
    text0 = page0.get_text()
    m_this = re.search(r'Question Id\s*:\s*' + raw_id, text0)
    
    if m_this and pno + 1 < len(doc):
        # Check if options start on next page
        if "Options :" not in text0[m_this.start():]:
            page1 = doc[pno + 1]
            text1 = page1.get_text()
            m_next_q = re.search(r'Question Number\s*:\s*\d+', text1)
            
            # Find bounds
            sr0 = page0.search_for(f"Question Id : {raw_id}")
            if not sr0:
                sr0 = page0.search_for(f"Question Number : {q.get('q_num')}")
            y0 = sr0[0].y0 - 15 if sr0 else 50
            
            y_next_end = 400
            if m_next_q:
                sr1 = page1.search_for(m_next_q.group(0))
                if sr1:
                    y_next_end = sr1[0].y0 - 10
                    
            try:
                rect0 = fitz.Rect(30, max(0, y0), page0.rect.width - 30, page0.rect.height)
                pix0 = page0.get_pixmap(clip=rect0, dpi=150)
                img0 = Image.frombytes("RGB", [pix0.width, pix0.height], pix0.samples)
                
                rect1 = fitz.Rect(30, 20, page1.rect.width - 30, min(page1.rect.height, max(60, y_next_end)))
                pix1 = page1.get_pixmap(clip=rect1, dpi=150)
                img1 = Image.frombytes("RGB", [pix1.width, pix1.height], pix1.samples)
                
                total_w = max(img0.width, img1.width)
                total_h = img0.height + img1.height
                stitched = Image.new("RGB", (total_w, total_h), (255, 255, 255))
                stitched.paste(img0, (0, 0))
                stitched.paste(img1, (0, img0.height))
                
                if total_w > 960:
                    stitched = stitched.resize((960, int(total_h * 960 / total_w)), Image.Resampling.LANCZOS)
                    
                stitched.save(card_full, "JPEG", quality=80, optimize=True)
                re_stitched_cards += 1
            except Exception as e:
                pass
                
    doc.close()

print(f"Updated options for {updated_opts} questions.")
print(f"Re-stitched multi-page cards for {re_stitched_cards} questions.")

# Save updated questions.json
with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

# Update questions_data.js
js_file = os.path.join(WORKSPACE_DIR, "data", "questions_data.js")
with open(js_file, "w", encoding="utf-8") as f:
    f.write("// IIT Madras Modern Application Development 1 (MAD 1 / AppDev1) Question Bank\n")
    f.write("window.MAD1_QUESTIONS = ")
    json.dump(questions, f, indent=2, ensure_ascii=False)
    f.write(";\n")

print(f"Successfully saved updated datasets!")
