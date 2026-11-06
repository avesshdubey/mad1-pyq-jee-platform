import fitz
import os
import re
import json

WORKSPACE_DIR = r"C:\Users\avesh\Desktop\mad1-pyq-jee-platform"
DATA_FILE = os.path.join(WORKSPACE_DIR, "data", "questions.json")
PYQS_DIR = r"C:\Users\avesh\Desktop\PYQS"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    questions = json.load(f)

paper_paths = {}
for root, dirs, files in os.walk(PYQS_DIR):
    for f in files:
        if f.lower().endswith(".pdf"):
            paper_paths[f] = os.path.join(root, f)

tested = 0
continuations = 0
issues = []

for q in questions:
    raw_id = str(q["raw_q_id"])
    pname = q["paper"]
    pno = q["page"] - 1
    if pname not in paper_paths:
        issues.append(f"Paper not found: {pname}")
        continue
    doc = fitz.open(paper_paths[pname])
    page0 = doc[pno]
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
        issues.append(f"QID not found: {q['id']} {raw_id} on page {pno+1}")
        continue
    qid_r = qid_rects[0]
    ql_rects = [r for r in page0.search_for("Question Label") if abs(r.y0 - qid_r.y0) < 80 and r.y0 >= qid_r.y0 - 20]
    top_y = (ql_rects[0].y1 + 4) if ql_rects else (qid_r.y1 + 4)
    
    next_q_rects = [r for r in page0.search_for("Question Number") if r.y0 > top_y + 30]
    sub_rects = [r for r in page0.search_for("Sub-Section Number") if r.y0 > top_y + 30]
    
    candidates = []
    if next_q_rects: candidates.append(min(r.y0 for r in next_q_rects) - 5)
    if sub_rects: candidates.append(min(r.y0 for r in sub_rects) - 5)
    bot_y = min(candidates) if candidates else (page0.rect.height - 20)
    
    txt_q0 = page0.get_text(clip=fitz.Rect(0, top_y, page0.rect.width, bot_y))
    has_cont = ("Options :" not in txt_q0) and (pno + 1 < len(doc))
    if has_cont:
        continuations += 1
    tested += 1

print(f"Tested {tested} / {len(questions)} questions. Found {continuations} multi-page continuations. Issues: {len(issues)}")
if issues:
    print("First 5 issues:", issues[:5])
