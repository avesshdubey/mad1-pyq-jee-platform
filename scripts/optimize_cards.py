import os
import json
from PIL import Image

BASE_DIR = r"C:\Users\avesh\Desktop\mad1-pyq-jee-platform"
DATA_FILE = os.path.join(BASE_DIR, "data", "questions.json")
CARDS_DIR = os.path.join(BASE_DIR, "assets", "q_cards")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    questions = json.load(f)

print(f"Loaded {len(questions)} questions. Optimizing cards to high-quality JPEG...")

used_raw_ids = set()
for q in questions:
    used_raw_ids.add(q["raw_q_id"])
    old_rel = q.get("card_image", "")
    old_full = os.path.join(BASE_DIR, old_rel.replace("/", os.sep))
    
    new_filename = f"mad1_card_{q['raw_q_id']}.jpg"
    new_full = os.path.join(CARDS_DIR, new_filename)
    new_rel = f"assets/q_cards/{new_filename}"
    
    if os.path.exists(old_full):
        try:
            with Image.open(old_full) as im:
                rgb_im = im.convert("RGB")
                w, h = rgb_im.size
                if w > 960:
                    new_h = int(h * 960 / w)
                    rgb_im = rgb_im.resize((960, new_h), Image.Resampling.LANCZOS)
                rgb_im.save(new_full, "JPEG", quality=80, optimize=True)
            # Remove old png if different
            if old_full != new_full and os.path.exists(old_full):
                os.remove(old_full)
            q["card_image"] = new_rel
        except Exception as e:
            print(f"Error on {old_rel}: {e}")

# Remove any unused .png cards in CARDS_DIR
removed_count = 0
for f in os.listdir(CARDS_DIR):
    if f.endswith(".png"):
        os.remove(os.path.join(CARDS_DIR, f))
        removed_count += 1
        
print(f"Removed {removed_count} unreferenced/old PNG cards.")

# Save updated questions.json
with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

# Update questions_data.js
js_file = os.path.join(BASE_DIR, "data", "questions_data.js")
with open(js_file, "w", encoding="utf-8") as f:
    f.write("// IIT Madras Modern Application Development 1 (MAD 1 / AppDev1) Question Bank\n")
    f.write("window.MAD1_QUESTIONS = ")
    json.dump(questions, f, indent=2, ensure_ascii=False)
    f.write(";\n")

# Check total size
total_mb = sum(os.path.getsize(os.path.join(CARDS_DIR, f)) for f in os.listdir(CARDS_DIR)) / (1024 * 1024)
print(f"Optimized {len(questions)} cards. Total assets/q_cards size: {total_mb:.2f} MB")
