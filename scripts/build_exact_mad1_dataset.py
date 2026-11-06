import fitz
import os
import re
import json
import glob
import hashlib
from PIL import Image

WORKSPACE_DIR = r"C:\Users\avesh\Desktop\mad1-pyq-jee-platform"
PYQS_DIR = r"C:\Users\avesh\Desktop\PYQS"

DATA_DIR = os.path.join(WORKSPACE_DIR, "data")
CARDS_DIR = os.path.join(WORKSPACE_DIR, "assets", "q_cards")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(CARDS_DIR, exist_ok=True)

# 4-Week Taxonomy Mapping for Modern Application Development 1 (IIT Madras BS Degree)
TAXONOMY = {
    "Week 1: Internet Architecture, HTTP & Network Calculations": [
        ("1.1 Web & Internet Basics (Client-Server Architecture, Protocols & Servers)", [
            "client-server", "client server", "web server", "dns", "domain name", "ip address", 
            "protocol", "tcp", "udp", "socket", "port", "architecture", "browser", "host", "packet"
        ]),
        ("1.2 Data Transmission, Bandwidth, RTT & Propagation Delay Calculations", [
            "bandwidth", "propagation delay", "transmission delay", "rtt", "round trip", "latency", 
            "throughput", "concurrent clients", "mbps", "kbps", "gbps", "bits per second", "bytes", 
            "data consumption", "packet size", "distance", "speed of light", "channel capacity", "motion calculations"
        ]),
        ("1.3 Character Encoding & Representation (ASCII, Unicode, UTF-8 & Binary)", [
            "ascii", "unicode", "utf-8", "utf-16", "utf-32", "character representation", "binary number", 
            "hexadecimal", "code point", "byte order mark", "bom", "encoding", "decoding", "2's complement"
        ]),
        ("1.4 HTTP Protocol, URLs, Request/Response Headers & Status Codes", [
            "http", "https", "url", "uri", "status code", "200 ok", "404 not found", "500 internal server error", 
            "301 moved", "302 found", "request header", "response header", "user-agent", "content-type", 
            "mime", "stateless", "http methods", "http request", "http response", "cookie", "session"
        ])
    ],
    "Week 2: HTML5, CSS3, Box Model & Form Controls": [
        ("2.1 HTML5 Elements, Semantic Tags & Document Structure", [
            "doctype", "html5", "semantic", "header", "footer", "nav", "article", "section", 
            "aside", "table", "tr", "td", "th", "ul", "ol", "li", "a href", "img src", "paragraph", 
            "heading", "dom", "tag", "element", "attribute"
        ]),
        ("2.2 HTML Forms, Input Types, Attributes & Form Submission", [
            "<form", "form method", "form action", "input type", "type=\"text\"", "type=\"password\"", 
            "type=\"submit\"", "type=\"checkbox\"", "type=\"radio\"", "select", "option", "textarea", 
            "button", "placeholder", "required", "enctype", "form submission", "name attribute", "value attribute"
        ]),
        ("2.3 CSS Selectors, Specificity & Cascade Rules", [
            "css selector", "class selector", "id selector", "pseudo-class", "pseudo-element", 
            "specificity", "cascade", "!important", "inheritance", "hover", "focus", "active", 
            "child selector", "descendant selector", "combinator", "attribute selector"
        ]),
        ("2.4 CSS Box Model & Layouts (Flexbox, Positioning & Spacing)", [
            "box model", "box-sizing", "content-box", "border-box", "margin", "padding", "border", 
            "display", "inline", "block", "inline-block", "none", "flex", "flexbox", "justify-content", 
            "align-items", "flex-direction", "position", "static", "relative", "absolute", "fixed", "sticky", 
            "float", "clear", "width", "height", "z-index"
        ]),
        ("2.5 Responsive Web Design & Media Queries", [
            "media query", "@media", "viewport", "responsive", "max-width", "min-width", 
            "screen", "breakpoint", "rem", "em", "vw", "vh", "fluid layout"
        ])
    ],
    "Week 3: Backend Python, Flask Essentials, Routing & Request Handling": [
        ("3.1 Python for Web & Command-Line Arguments", [
            "sys.argv", "sys.argv[0]", "sys.argv[1]", "sys.argv[2]", "command-line", "command line", 
            "script argument", "len(sys.argv)", "import sys", "python web"
        ]),
        ("3.2 Flask Application Setup & App Configuration", [
            "flask(__name__)", "flask(__name__)", "app = flask", "app.run", "debug=true", 
            "flask configuration", "wsgi", "microframework", "instance"
        ]),
        ("3.3 Routing, Dynamic URL Converters & View Functions", [
            "@app.route", "app.route", "url_for", "converter", "<int:", "<string:", "<float:", 
            "<path:", "dynamic route", "endpoint", "view function", "rule"
        ]),
        ("3.4 HTTP Methods in Flask (GET, POST & Handling)", [
            "methods=['get'", "methods=['post'", "methods=[\"get\"", "methods=[\"post\"", 
            "request.method == 'post'", "request.method == 'get'", "methods"
        ]),
        ("3.5 Flask Request Object & Data Extraction", [
            "request.args", "request.form", "request.values", "request.headers", "request.data", 
            "request.files", "request.cookies", "get parameters", "query string", "post data"
        ]),
        ("3.6 Flask Responses, Redirects & Error Handling", [
            "redirect(", "abort(", "make_response(", "jsonify(", "render_template_string", 
            "response object", "status code", "custom error", "@app.errorhandler", "404 handler"
        ])
    ],
    "Week 4: Jinja2 Templating, Dynamic Rendering, SQLite & CRUD Applications": [
        ("4.1 Jinja2 Templating Basics (Variables & Control Flow)", [
            "jinja", "jinja2", "render_template", "{{", "}}", "{%", "%}", "{% if", "{% endif", 
            "{% for", "{% endfor", "loop.index", "template variable", "expression", "delimiters"
        ]),
        ("4.2 Jinja2 Filters, Macros & Template Inheritance", [
            "{% extends", "{% block", "{% endblock", "template inheritance", "super()", 
            "filter", "|upper", "|lower", "|length", "|default", "macro", "include"
        ]),
        ("4.3 SQLite Database Fundamentals & SQL Queries", [
            "sqlite", "sqlite3", "sql", "select ", "insert into", "update ", "delete from", 
            "create table", "primary key", "foreign key", "where ", "join", "schema", "table"
        ]),
        ("4.4 Database Integration in Flask (sqlite3, Cursor & Connection)", [
            "sqlite3.connect", "cursor", "cursor.execute", "cursor.fetchall", "cursor.fetchone", 
            "db.commit", "db.close", "row_factory", "connection", "parameterized query", "?"
        ]),
        ("4.5 Full-Stack CRUD Workflows & Form Processing", [
            "crud", "create, read, update, delete", "form processing", "validation", "database persistence", 
            "data flow", "model-view", "mvc", "sqlite database", "app.db"
        ])
    ]
}

def classify_question(text):
    text_lower = text.lower()
    
    # Priority Database / SQLite / SQL
    if re.search(r'\b(sqlite|sqlite3|cursor|fetchall|fetchone|cursor\.execute|sql\s+query|create\s+table|foreign\s+key|primary\s+key)\b', text_lower):
        if re.search(r'\b(sqlite3\.connect|cursor|connection|commit|fetchall|fetchone)\b', text_lower):
            return "Week 4: Jinja2 Templating, Dynamic Rendering, SQLite & CRUD Applications", "4.4 Database Integration in Flask (sqlite3, Cursor & Connection)"
        elif re.search(r'\b(select|insert|update|delete|where|from\s+\w+)\b', text_lower):
            return "Week 4: Jinja2 Templating, Dynamic Rendering, SQLite & CRUD Applications", "4.3 SQLite Database Fundamentals & SQL Queries"
        else:
            return "Week 4: Jinja2 Templating, Dynamic Rendering, SQLite & CRUD Applications", "4.5 Full-Stack CRUD Workflows & Form Processing"

    # Priority Jinja2 / Templates
    if re.search(r'(\{\%|\{\{|\%\}|\}\}|jinja|render_template|template\s+inheritance|\{\%\s*extends|\{\%\s*block)', text_lower):
        if re.search(r'(\{\%\s*extends|\{\%\s*block|\{\%\s*endblock|template\s+inheritance|super\(\)|filter|macro)', text_lower):
            return "Week 4: Jinja2 Templating, Dynamic Rendering, SQLite & CRUD Applications", "4.2 Jinja2 Filters, Macros & Template Inheritance"
        else:
            return "Week 4: Jinja2 Templating, Dynamic Rendering, SQLite & CRUD Applications", "4.1 Jinja2 Templating Basics (Variables & Control Flow)"

    # Priority Command-line sys.argv
    if "sys.argv" in text_lower or re.search(r'\bsys\.argv\[', text_lower):
        return "Week 3: Backend Python, Flask Essentials, Routing & Request Handling", "3.1 Python for Web & Command-Line Arguments"

    # Priority Flask Request Object
    if re.search(r'\b(request\.args|request\.form|request\.values|request\.headers|request\.method)\b', text_lower):
        return "Week 3: Backend Python, Flask Essentials, Routing & Request Handling", "3.5 Flask Request Object & Data Extraction"

    # Priority Flask Redirect & Responses
    if re.search(r'\b(redirect\(|abort\(|make_response\(|jsonify\(|errorhandler)\b', text_lower):
        return "Week 3: Backend Python, Flask Essentials, Routing & Request Handling", "3.6 Flask Responses, Redirects & Error Handling"

    # Priority Flask Routing & Methods
    if re.search(r'(@app\.route|methods\s*=|url_for|<int:|<string:|<float:)', text_lower):
        if "methods" in text_lower or "post" in text_lower or "get" in text_lower:
            return "Week 3: Backend Python, Flask Essentials, Routing & Request Handling", "3.4 HTTP Methods in Flask (GET, POST & Handling)"
        else:
            return "Week 3: Backend Python, Flask Essentials, Routing & Request Handling", "3.3 Routing, Dynamic URL Converters & View Functions"

    # General Flask
    if re.search(r'\b(flask|app\s*=\s*flask|app\.run)\b', text_lower):
        return "Week 3: Backend Python, Flask Essentials, Routing & Request Handling", "3.2 Flask Application Setup & App Configuration"

    # Priority CSS Box Model / Flexbox / Positioning
    if re.search(r'\b(box\s*model|box-sizing|border-box|content-box|flexbox|display:\s*flex|margin|padding|border|justify-content|align-items|position:\s*(absolute|relative|fixed|sticky)|z-index)\b', text_lower):
        return "Week 2: HTML5, CSS3, Box Model & Form Controls", "2.4 CSS Box Model & Layouts (Flexbox, Positioning & Spacing)"

    # Priority CSS Selectors & Cascade
    if re.search(r'\b(css\s*selector|specificity|cascade|pseudo-class|pseudo-element|!important|hover|active|focus)\b', text_lower) or re.search(r'\b(selector|combinator)\b', text_lower):
        return "Week 2: HTML5, CSS3, Box Model & Form Controls", "2.3 CSS Selectors, Specificity & Cascade Rules"

    # Priority Media Queries & Responsive
    if re.search(r'(@media|media\s*query|viewport|responsive\s*web|breakpoint|max-width|min-width)', text_lower):
        return "Week 2: HTML5, CSS3, Box Model & Form Controls", "2.5 Responsive Web Design & Media Queries"

    # Priority HTML Forms
    if re.search(r'(<form|form\s+method|input\s+type|textarea|select|placeholder|action=)', text_lower):
        return "Week 2: HTML5, CSS3, Box Model & Form Controls", "2.2 HTML Forms, Input Types, Attributes & Form Submission"

    # Priority HTML5 Elements
    if re.search(r'(<html|<doctype|<div|<span|<table|<tr|<td|<p>|<a\s+href|<img|<nav|<article|<section|<header|<footer|semantic)', text_lower):
        return "Week 2: HTML5, CSS3, Box Model & Form Controls", "2.1 HTML5 Elements, Semantic Tags & Document Structure"

    # Priority Network Calculations: Bandwidth, Delay, RTT
    if re.search(r'\b(bandwidth|propagation\s+delay|transmission\s+delay|rtt|round\s+trip|concurrent\s+client|latency|throughput|mbps|kbps|gbps|packet\s+size|motion\s+calculation)\b', text_lower):
        return "Week 1: Internet Architecture, HTTP & Network Calculations", "1.2 Data Transmission, Bandwidth, RTT & Propagation Delay Calculations"

    # Priority Character Encoding: ASCII, Unicode, UTF-8
    if re.search(r'\b(ascii|unicode|utf-8|utf-16|character\s+representation|binary\s+number|hexadecimal|code\s+point|byte\s+order\s+mark|bom)\b', text_lower):
        return "Week 1: Internet Architecture, HTTP & Network Calculations", "1.3 Character Encoding & Representation (ASCII, Unicode, UTF-8 & Binary)"

    # Priority HTTP Protocol & Headers
    if re.search(r'\b(http|https|url|uri|status\s+code|200\s+ok|404\s+not\s+found|500\s+internal|user-agent|content-type|mime|request\s+header|response\s+header)\b', text_lower):
        return "Week 1: Internet Architecture, HTTP & Network Calculations", "1.4 HTTP Protocol, URLs, Request/Response Headers & Status Codes"

    # General Web / Client Server
    if re.search(r'\b(client-server|web\s+server|dns|domain\s+name|ip\s+address|tcp|port|socket|browser|host)\b', text_lower):
        return "Week 1: Internet Architecture, HTTP & Network Calculations", "1.1 Web & Internet Basics (Client-Server Architecture, Protocols & Servers)"

    # Best-effort scoring across all categories
    best_score = 0
    best_week = "Week 1: Internet Architecture, HTTP & Network Calculations"
    best_sub = "1.1 Web & Internet Basics (Client-Server Architecture, Protocols & Servers)"
    
    for week_name, subtopics in TAXONOMY.items():
        for sub_name, keywords in subtopics:
            score = 0
            for kw in keywords:
                if kw in text_lower:
                    score += len(kw)
            if score > best_score:
                best_score = score
                best_week = week_name
                best_sub = sub_name
                
    return best_week, best_sub

def find_mad1_boundaries(doc):
    total_pages = len(doc)
    start_p = None
    y_start = 0
    end_p = total_pages - 1
    y_end = 999999
    is_legacy = False
    
    # Standard Section Detection
    for pno in range(total_pages):
        text = doc[pno].get_text()
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        for idx, line in enumerate(lines):
            # Modern TCS iON: Section Id : with line above being Appdev1
            if line == "Section Id :" and idx > 0:
                sec_name = lines[idx-1]
                # Match Appdev1, AppDev1, AppDev-1, but strictly NOT Appdev2 or AppDev-2!
                sec_lower = sec_name.lower()
                if any(k in sec_lower for k in ["appdev1", "appdev-1", "app dev 1", "mad1", "mad 1"]) and "appdev2" not in sec_lower and "appdev-2" not in sec_lower:
                    start_p = pno
                    sr = doc[pno].search_for("Section Id :")
                    y_start = min((r.y0 for r in sr), default=0)
                    is_legacy = False
                    break
            # Legacy 2022 format: line == 'AppDev-1' followed by 'Number of Questions :'
            elif line.lower() in ["appdev-1", "appdev1"] and idx + 1 < len(lines) and "number of questions" in lines[idx+1].lower():
                start_p = pno
                sr = doc[pno].search_for(line)
                y_start = min((r.y0 for r in sr), default=0)
                is_legacy = True
                break
        if start_p is not None:
            break
            
    if start_p is None:
        return None, 0, None, 0
        
    for pno in range(start_p, total_pages):
        text = doc[pno].get_text()
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        for idx, line in enumerate(lines):
            if not is_legacy:
                if line == "Section Id :" and idx > 0:
                    sec_name = lines[idx-1]
                    sec_lower = sec_name.lower()
                    if not (any(k in sec_lower for k in ["appdev1", "appdev-1", "app dev 1", "mad1", "mad 1"]) and "appdev2" not in sec_lower and "appdev-2" not in sec_lower):
                        sr = doc[pno].search_for("Section Id :")
                        if pno == start_p:
                            sr = [r for r in sr if r.y0 > y_start + 100]
                        if sr:
                            y_end = min(r.y0 for r in sr) - 10
                            end_p = pno
                            return start_p, y_start, end_p, y_end
            else:
                if line == "Number of Questions :" and (pno > start_p or (pno == start_p and idx > 3)):
                    sec_name = lines[idx-1] if idx > 0 else ""
                    if sec_name.lower() not in ["appdev-1", "appdev1"]:
                        sr = doc[pno].search_for("Number of Questions :")
                        if pno == start_p:
                            sr = [r for r in sr if r.y0 > y_start + 100]
                        if sr:
                            y_end = min(r.y0 for r in sr) - 10
                            end_p = pno
                            return start_p, y_start, end_p, y_end
                            
    return start_p, y_start, total_pages - 1, 999999

def clean_extracted_text(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    cleaned = []
    skip_headers = [
        "Question Number :", "Question Id :", "Question Type :", "Correct Marks :",
        "Question Label :", "Response Type :", "Evaluation Required", "Show Word Count :",
        "Answers Type :", "Text Areas :", "Section Id :", "Section Number :", "Section type :",
        "Mandatory or Optional", "Number of Questions", "Section Marks :", "Section Negative Marks",
        "Group All Questions", "Enable Mark as Answered", "Sub-Section Number", "Sub-Section Id",
        "Question Shuffling Allowed", "Options :", "Online Mandatory or Optional",
        "THIS IS QUESTION PAPER FOR THE SUBJECT", "ARE YOU SURE YOU HAVE TO WRITE EXAM",
        "CROSS CHECK YOUR HALL TICKET"
    ]
    
    possible_ans = []
    in_ans = False
    
    for l in lines:
        if "Possible Answers :" in l:
            in_ans = True
            continue
        if in_ans:
            if re.match(r'^\d+(\.\d+)?(\s*to\s*\d+(\.\d+)?)?$', l) or re.match(r'^-?\d+(\.\d+)?', l):
                possible_ans.append(l)
            else:
                in_ans = False
        
        if any(l.startswith(h) for h in skip_headers):
            continue
        if re.match(r'^\d{13}\.$', l):
            continue
        cleaned.append(l)
        
    t = "\n".join(cleaned)
    t = re.sub(r'THIS IS QUESTION PAPER FOR THE SUBJECT.*', '', t)
    t = re.sub(r'ARE YOU SURE YOU HAVE TO WRITE EXAM.*', '', t)
    t = re.sub(r'CROSS CHECK YOUR HALL TICKET.*', '', t)
    t = re.sub(r'\(IF IT IS NOT THE CORRECT SUBJECT.*', '', t)
    t = re.sub(r'\n\s*\n+', '\n', t).strip()
    return t, possible_ans

def process_paper(pdf_path):
    paper_name = os.path.basename(pdf_path)
    try:
        doc = fitz.open(pdf_path)
    except Exception:
        return []
        
    start_pno, y_start_page, end_pno, y_end_page = find_mad1_boundaries(doc)
    if start_pno is None:
        doc.close()
        return []
        
    extracted_questions = []
    
    for pno in range(start_pno, end_pno + 1):
        page = doc[pno]
        text_page = page.get_text()
        
        # Find all questions on this page
        q_matches = list(re.finditer(r'Question Number\s*:\s*(\d+)\s+Question Id\s*:\s*(\d+)\s+Question Type\s*:\s*(\w+)', text_page))
        if not q_matches:
            continue
            
        for idx, m in enumerate(q_matches):
            q_num = m.group(1)
            raw_q_id = m.group(2)
            q_type = m.group(3)
            
            # Question coordinates
            sr = page.search_for(m.group(0))
            if not sr:
                continue
            y0 = sr[0].y0
            
            # Boundary checks
            if pno == start_pno and y0 < y_start_page:
                continue
            if pno == end_pno and y0 > y_end_page:
                continue
                
            # Question bottom boundary
            if idx + 1 < len(q_matches):
                next_sr = page.search_for(q_matches[idx+1].group(0))
                y1 = next_sr[0].y0 if next_sr else page.rect.height
            else:
                y1 = page.rect.height
                if pno == end_pno and y_end_page < page.rect.height:
                    y1 = min(y1, y_end_page)
                    
            # Extract section text snippet
            txt_snippet = text_page[m.start():]
            if idx + 1 < len(q_matches):
                txt_snippet = text_page[m.start():q_matches[idx+1].start()]
                
            # Filter 0-mark questions & confirmation prompts
            m_marks = re.search(r'Correct Marks\s*:\s*([\d.]+)', txt_snippet)
            marks = float(m_marks.group(1)) if m_marks else 0.0
            
            if marks <= 0 or "ARE YOU SURE YOU HAVE TO WRITE EXAM" in txt_snippet or "THIS IS QUESTION PAPER FOR THE SUBJECT" in txt_snippet:
                continue
                
            # Clean text and possible answers
            cleaned_stem, possible_ans = clean_extracted_text(txt_snippet)
            
            # Extract Options
            options = []
            option_matches = list(re.finditer(r'(\d{13})\.\s*([^\n\r]*)', txt_snippet))
            for opt_m in option_matches:
                opt_id = opt_m.group(1)
                opt_txt = opt_m.group(2).strip()
                options.append({
                    "option_id": opt_id,
                    "text": opt_txt
                })
                
            # Correct answer keys
            correct_keys = []
            if q_type == "SA":
                correct_keys = possible_ans
            elif options:
                correct_keys = [options[0]["option_id"]]
                
            # Multi-page question expansion: check if question choices continue on next page
            continuation_pno = None
            if idx == len(q_matches) - 1 and pno < end_pno:
                next_page = doc[pno + 1]
                next_txt = next_page.get_text()
                next_q_matches = list(re.finditer(r'Question Number\s*:\s*\d+', next_txt))
                # If next page has no new question immediately at top, or options appear before first question
                if not next_q_matches or (next_q_matches and next_page.search_for(next_q_matches[0].group(0))[0].y0 > 150):
                    continuation_pno = pno + 1
                    
            # Crop 150-DPI Visual Card
            card_filename = f"mad1_card_{raw_q_id}.png"
            card_filepath = os.path.join(CARDS_DIR, card_filename)
            card_relpath = f"assets/q_cards/{card_filename}"
            
            try:
                rect0 = fitz.Rect(30, max(0, y0 - 10), page.rect.width - 30, min(page.rect.height, y1 + 5))
                pix0 = page.get_pixmap(clip=rect0, dpi=150)
                img0 = Image.frombytes("RGB", [pix0.width, pix0.height], pix0.samples)
                
                if continuation_pno is not None:
                    next_page = doc[continuation_pno]
                    next_txt = next_page.get_text()
                    next_q_matches = list(re.finditer(r'Question Number\s*:\s*\d+', next_txt))
                    if next_q_matches:
                        y_next_end = next_page.search_for(next_q_matches[0].group(0))[0].y0 - 10
                    else:
                        y_next_end = min(next_page.rect.height, 400)
                        
                    rect1 = fitz.Rect(30, 20, next_page.rect.width - 30, max(50, y_next_end))
                    pix1 = next_page.get_pixmap(clip=rect1, dpi=150)
                    img1 = Image.frombytes("RGB", [pix1.width, pix1.height], pix1.samples)
                    
                    # Vertical stitch
                    total_w = max(img0.width, img1.width)
                    total_h = img0.height + img1.height
                    stitched = Image.new("RGB", (total_w, total_h), (255, 255, 255))
                    stitched.paste(img0, (0, 0))
                    stitched.paste(img1, (0, img0.height))
                    stitched.save(card_filepath, "PNG", optimize=True)
                else:
                    img0.save(card_filepath, "PNG", optimize=True)
            except Exception as e:
                pass
                
            week, subtopic = classify_question(cleaned_stem)
            
            q_record = {
                "raw_q_id": raw_q_id,
                "q_num": q_num,
                "paper": paper_name,
                "page": pno + 1,
                "question_type": q_type,
                "marks": marks,
                "question_text": cleaned_stem,
                "options": options,
                "correct_answer": correct_keys,
                "card_image": card_relpath,
                "week": week,
                "subtopic": subtopic
            }
            extracted_questions.append(q_record)
            
    doc.close()
    return extracted_questions

def main():
    print("=== Scanning all PDFs in PYQS for MAD 1 (AppDev1) ===")
    pdf_files = []
    for root, dirs, files in os.walk(PYQS_DIR):
        for f in files:
            if f.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(root, f))
                
    print(f"Total PDFs found: {len(pdf_files)}")
    all_raw_questions = []
    papers_with_mad1 = 0
    
    for idx, pdf in enumerate(pdf_files):
        qs = process_paper(pdf)
        if qs:
            papers_with_mad1 += 1
            all_raw_questions.extend(qs)
            print(f"[{papers_with_mad1:2d}] {os.path.basename(pdf)} -> Extracted {len(qs)} questions")
            
    print(f"\nTotal raw questions extracted across {papers_with_mad1} papers: {len(all_raw_questions)}")
    
    # Deduplication Engine
    print("\n=== Running Deduplication Engine ===")
    unique_questions = {}
    fingerprint_map = {}
    
    for q in all_raw_questions:
        norm_stem = re.sub(r'\s+', ' ', q["question_text"].lower()).strip()
        # Clean special chars for fingerprint
        norm_key = re.sub(r'[^a-z0-9]', '', norm_stem)
        
        # If stem is very short (e.g. image-only questions), use options fingerprint or card hash
        if len(norm_key) < 20:
            opt_str = "".join([re.sub(r'[^a-z0-9]', '', o["text"].lower()) for o in q["options"]])
            norm_key = f"short_{q['question_type']}_{opt_str}"
            if len(norm_key) < 15:
                # Use raw question id or marks + page
                norm_key = f"img_{q['marks']}_{q['raw_q_id']}"
                
        if norm_key in fingerprint_map:
            existing_id = fingerprint_map[norm_key]
            existing = unique_questions[existing_id]
            if q["paper"] not in existing["source_papers"]:
                existing["source_papers"].append(q["paper"])
            # Update options if current has fuller text
            if len(q["options"]) > len(existing["options"]):
                existing["options"] = q["options"]
            if len(q["question_text"]) > len(existing["question_text"]):
                existing["question_text"] = q["question_text"]
        else:
            new_id = f"MAD1_{len(unique_questions) + 1:03d}"
            q["id"] = new_id
            q["source_papers"] = [q["paper"]]
            fingerprint_map[norm_key] = new_id
            unique_questions[new_id] = q

    deduped_list = list(unique_questions.values())
    print(f"Total unique questions after deduplication: {len(deduped_list)}")
    
    # Week breakdown
    week_counts = {}
    subtopic_counts = {}
    for q in deduped_list:
        w = q["week"].split(":")[0].strip()
        week_counts[w] = week_counts.get(w, 0) + 1
        st = q["subtopic"]
        subtopic_counts[st] = subtopic_counts.get(st, 0) + 1
        
    print("\n=== Week Distribution ===")
    for w in sorted(week_counts.keys()):
        print(f"  {w}: {week_counts[w]} questions")
        
    print("\n=== Subtopic Breakdown ===")
    for st, count in sorted(subtopic_counts.items(), key=lambda x: -x[1]):
        print(f"  {st}: {count} questions")
        
    # Save datasets
    questions_json_path = os.path.join(DATA_DIR, "questions.json")
    with open(questions_json_path, "w", encoding="utf-8") as f:
        json.dump(deduped_list, f, indent=2, ensure_ascii=False)
    print(f"\nSaved questions dataset: {questions_json_path}")
    
    stats_json_path = os.path.join(DATA_DIR, "stats.json")
    stats = {
        "total_papers_scanned": len(pdf_files),
        "papers_with_mad1": papers_with_mad1,
        "total_raw_questions": len(all_raw_questions),
        "total_unique_questions": len(deduped_list),
        "week_counts": week_counts,
        "subtopic_counts": subtopic_counts
    }
    with open(stats_json_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    print(f"Saved stats dataset: {stats_json_path}")
    
    # Generate standalone JS bundle for offline/CBT app
    js_bundle_path = os.path.join(DATA_DIR, "questions_data.js")
    with open(js_bundle_path, "w", encoding="utf-8") as f:
        f.write("// IIT Madras Modern Application Development 1 (MAD 1 / AppDev1) Question Bank\n")
        f.write("window.MAD1_QUESTIONS = ")
        json.dump(deduped_list, f, indent=2, ensure_ascii=False)
        f.write(";\n")
    print(f"Saved standalone JS bundle: {js_bundle_path}")

if __name__ == "__main__":
    main()
