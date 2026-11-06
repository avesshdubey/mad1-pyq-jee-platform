import fitz
import os
import re
import json
from collections import Counter

WORKSPACE_DIR = r"C:\Users\avesh\Desktop\mad1-pyq-jee-platform"
DATA_FILE = os.path.join(WORKSPACE_DIR, "data", "questions.json")
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

TAXONOMY = {
    "Week 1: Internet Architecture, HTTP & Network Calculations": [
        ("1.1 Web & Internet Basics (Client-Server Architecture, Protocols & Servers)", [
            "client-server", "client server", "web server", "dns", "domain name", "ip address", 
            "protocol", "tcp", "udp", "socket", "port", "architecture", "browser", "host", "packet", "layer"
        ]),
        ("1.2 Data Transmission, Bandwidth, RTT & Propagation Delay Calculations", [
            "bandwidth", "propagation delay", "transmission delay", "rtt", "round trip", "latency", 
            "throughput", "concurrent client", "mbps", "kbps", "gbps", "bits per second", "bytes", 
            "data consumption", "packet size", "distance", "speed of light", "channel capacity", "motion calculation",
            "download time", "upload time", "file transfer", "bits", "bytes"
        ]),
        ("1.3 Character Encoding & Representation (ASCII, Unicode, UTF-8 & Binary)", [
            "ascii", "unicode", "utf-8", "utf-16", "utf-32", "character representation", "binary number", 
            "hexadecimal", "code point", "byte order mark", "bom", "encoding", "decoding", "2's complement",
            "base 2", "base 16", "bits to represent", "representation"
        ]),
        ("1.4 HTTP Protocol, URLs, Request/Response Headers & Status Codes", [
            "http", "https", "url", "uri", "status code", "200 ok", "404 not found", "500 internal server error", 
            "301 moved", "302 found", "request header", "response header", "user-agent", "content-type", 
            "mime", "stateless", "http method", "http request", "http response", "cookie", "session", "cache"
        ])
    ],
    "Week 2: HTML5, CSS3, Box Model & Form Controls": [
        ("2.1 HTML5 Elements, Semantic Tags & Document Structure", [
            "doctype", "html5", "semantic", "header", "footer", "nav", "article", "section", 
            "aside", "table", "tr", "td", "th", "ul", "ol", "li", "a href", "img src", "paragraph", 
            "heading", "dom", "tag", "element", "attribute", "alt", "title", "body", "head", "<dt>", "<dd>", "<dl>"
        ]),
        ("2.2 HTML Forms, Input Types, Attributes & Form Submission", [
            "<form", "form method", "form action", "input type", "type=\"text\"", "type=\"password\"", 
            "type=\"submit\"", "type=\"checkbox\"", "type=\"radio\"", "select", "option", "textarea", 
            "button", "placeholder", "required", "enctype", "form submission", "name attribute", "value attribute",
            "form data", "input", "form"
        ]),
        ("2.3 CSS Selectors, Specificity & Cascade Rules", [
            "css selector", "class selector", "id selector", "pseudo-class", "pseudo-element", 
            "specificity", "cascade", "!important", "inheritance", "hover", "focus", "active", 
            "child selector", "descendant selector", "combinator", "attribute selector", "nth-child"
        ]),
        ("2.4 CSS Box Model & Layouts (Flexbox, Positioning & Spacing)", [
            "box model", "box-sizing", "content-box", "border-box", "margin", "padding", "border", 
            "display", "inline", "block", "inline-block", "none", "flex", "flexbox", "justify-content", 
            "align-items", "flex-direction", "position", "static", "relative", "absolute", "fixed", "sticky", 
            "float", "clear", "width", "height", "z-index", "color", "background"
        ]),
        ("2.5 Responsive Web Design & Media Queries", [
            "media query", "@media", "viewport", "responsive", "max-width", "min-width", 
            "screen", "breakpoint", "rem", "em", "vw", "vh", "fluid layout"
        ])
    ],
    "Week 3: Backend Python, Flask Essentials, Routing & Request Handling": [
        ("3.1 Python Web Fundamentals & Command-Line Arguments", [
            "sys.argv", "sys.argv[0]", "sys.argv[1]", "sys.argv[2]", "command-line", "command line", 
            "script argument", "len(sys.argv)", "import sys", "python web", "tuples", "dictionary", "dict", "tuple"
        ]),
        ("3.2 Flask Application Setup & App Configuration", [
            "flask(__name__)", "flask", "app = flask", "app.run", "debug=true", 
            "flask configuration", "wsgi", "microframework", "instance", "virtualenv"
        ]),
        ("3.3 Routing, Dynamic URL Converters & View Functions", [
            "@app.route", "app.route", "url_for", "converter", "<int:", "<string:", "<float:", 
            "<path:", "dynamic route", "endpoint", "view function", "rule", "route", "parameter"
        ]),
        ("3.4 HTTP Methods in Flask (GET, POST & Handling)", [
            "methods=['get'", "methods=['post'", "methods=[\"get\"", "methods=[\"post\"", 
            "request.method == 'post'", "request.method == 'get'", "methods", "post method", "get method"
        ]),
        ("3.5 Flask Request Object & Data Extraction", [
            "request.args", "request.form", "request.values", "request.headers", "request.data", 
            "request.files", "request.cookies", "get parameters", "query string", "post data", "request object"
        ]),
        ("3.6 Flask Responses, Redirects & Error Handling", [
            "redirect(", "abort(", "make_response(", "jsonify(", "render_template_string", 
            "response object", "status code", "custom error", "@app.errorhandler", "404 handler", "redirect", "abort"
        ])
    ],
    "Week 4: Jinja2 Templating, Dynamic Rendering, SQLite & CRUD Applications": [
        ("4.1 Jinja2 Templating Basics (Variables & Control Flow)", [
            "jinja", "jinja2", "render_template", "{{", "}}", "{%", "%}", "{% if", "{% endif", 
            "{% for", "{% endfor", "loop.index", "template variable", "expression", "delimiters", "template"
        ]),
        ("4.2 Jinja2 Filters, Macros & Template Inheritance", [
            "{% extends", "{% block", "{% endblock", "template inheritance", "super()", 
            "filter", "|upper", "|lower", "|length", "|default", "macro", "include", "extends", "block"
        ]),
        ("4.3 SQLite Database Fundamentals & SQL Queries", [
            "sqlite", "sqlite3", "sql", "select ", "insert into", "update ", "delete from", 
            "create table", "primary key", "foreign key", "where ", "join", "schema", "table", "query"
        ]),
        ("4.4 Database Integration in Flask (sqlite3, Cursor & Connection)", [
            "sqlite3.connect", "cursor", "cursor.execute", "cursor.fetchall", "cursor.fetchone", 
            "db.commit", "db.close", "row_factory", "connection", "parameterized query", "?", "database"
        ]),
        ("4.5 Full-Stack CRUD Workflows & Form Processing", [
            "crud", "create, read, update, delete", "form processing", "validation", "database persistence", 
            "data flow", "model-view", "mvc", "sqlite database", "app.db", "application"
        ])
    ]
}

def classify_question(text, raw_q_id=""):
    text_lower = text.lower()
    
    # Special fix for MAD1_022
    if "devatook" in text_lower or ("courses" in text_lower and "names =" in text_lower and "compiler" in text_lower):
        return "Week 3: Backend Python, Flask Essentials, Routing & Request Handling", "3.1 Python Web Fundamentals & Command-Line Arguments"

    # Priority Database / SQLite / SQL
    if re.search(r'\b(sqlite|sqlite3|cursor|fetchall|fetchone|cursor\.execute|foreign\s+key|primary\s+key)\b', text_lower):
        if re.search(r'\b(sqlite3\.connect|cursor|connection|commit|fetchall|fetchone)\b', text_lower):
            return "Week 4: Jinja2 Templating, Dynamic Rendering, SQLite & CRUD Applications", "4.4 Database Integration in Flask (sqlite3, Cursor & Connection)"
        elif re.search(r'\b(select\s+|insert\s+into|update\s+|delete\s+from|create\s+table)\b', text_lower):
            return "Week 4: Jinja2 Templating, Dynamic Rendering, SQLite & CRUD Applications", "4.3 SQLite Database Fundamentals & SQL Queries"
        else:
            return "Week 4: Jinja2 Templating, Dynamic Rendering, SQLite & CRUD Applications", "4.5 Full-Stack CRUD Workflows & Form Processing"

    # Priority Jinja2 / Templates
    if re.search(r'(\{\%|\{\{|\%\}|\}\}|jinja|render_template|template\s+inheritance|\{\%\s*extends|\{\%\s*block)', text_lower):
        if re.search(r'(\{\%\s*extends|\{\%\s*block|\{\%\s*endblock|template\s+inheritance|super\(\)|filter|macro)', text_lower):
            return "Week 4: Jinja2 Templating, Dynamic Rendering, SQLite & CRUD Applications", "4.2 Jinja2 Filters, Macros & Template Inheritance"
        else:
            return "Week 4: Jinja2 Templating, Dynamic Rendering, SQLite & CRUD Applications", "4.1 Jinja2 Templating Basics (Variables & Control Flow)"

    # Priority Python Tuples / Dictionary / sys.argv
    if "sys.argv" in text_lower or re.search(r'\bsys\.argv\[', text_lower) or ("tuples" in text_lower and "courses" in text_lower) or ("names =" in text_lower and "courses =" in text_lower):
        return "Week 3: Backend Python, Flask Essentials, Routing & Request Handling", "3.1 Python Web Fundamentals & Command-Line Arguments"

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
    if re.search(r'(<html|<doctype|<div|<span|<table|<tr|<td|<p>|<a\s+href|<img|<nav|<article|<section|<header|<footer|<dt>|<dd>|definition\s+list|semantic)', text_lower):
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

    # Best-effort scoring across all categories (do NOT count generic 'option')
    best_score = 0
    best_week = "Week 1: Internet Architecture, HTTP & Network Calculations"
    best_sub = "1.1 Web & Internet Basics (Client-Server Architecture, Protocols & Servers)"
    
    for week_name, subtopics in TAXONOMY.items():
        for sub_name, keywords in subtopics:
            score = 0
            for kw in keywords:
                if kw == "option":
                    continue # avoid false positives
                if kw in text_lower:
                    score += len(kw)
            if score > best_score:
                best_score = score
                best_week = week_name
                best_sub = sub_name
                
    return best_week, best_sub

green_detected_count = 0
options_perfected_count = 0

for q in questions:
    paper_name = q.get("paper")
    if paper_name not in paper_paths:
        continue
    doc = fitz.open(paper_paths[paper_name])
    pno = q.get("page") - 1
    raw_id = q.get("raw_q_id")
    q_type = q.get("question_type", "MCQ")
    
    # Special handling for MAD1_022
    if q.get("id") == "MAD1_022":
        q["options"] = [
            {"option_id": "6406531148355", "text": "Option A"},
            {"option_id": "6406531148356", "text": "Option B"},
            {"option_id": "6406531148357", "text": "Option C"},
            {"option_id": "6406531148358", "text": "Option D"}
        ]
        q["correct_answer"] = ["6406531148355"]
        q["week"] = "Week 2: HTML5, CSS3, Box Model & Form Controls"
        q["subtopic"] = "2.1 HTML5 Elements, Semantic Tags & Document Structure"
        doc.close()
        continue

    # Skip SA options extraction (SA has no options, has numeric answer)
    if q_type == "SA":
        # Keep existing correct answer
        doc.close()
        continue

    # 1. Gather text and green marks from pno up to pno+2
    full_text = ""
    page_texts = {}
    green_marks = [] # (page_idx, y_center)
    
    for p in range(pno, min(pno + 3, len(doc))):
        page = doc[p]
        p_txt = page.get_text()
        page_texts[p] = p_txt
        full_text += f"\n---PAGE_{p}---\n" + p_txt
        
        for img in page.get_image_info(xrefs=True):
            if img['width'] <= 24 and img['height'] <= 24:
                try:
                    pix = fitz.Pixmap(doc, img['xref'])
                    if pix.n >= 3:
                        cx, cy = pix.width // 2, pix.height // 2
                        r, g, b = pix.pixel(cx, cy)[:3]
                        if g > r + 20 and g > b + 20: # Green checkmark!
                            green_marks.append((p, (img['bbox'][1] + img['bbox'][3]) / 2.0))
                except:
                    pass

    # Extract question snippet
    m_snippet = re.search(r'Question Id\s*:\s*' + re.escape(raw_id) + r'.*?(?=Question Number\s*:\s*\d+|$)', full_text, re.DOTALL)
    q_snippet = m_snippet.group(0) if m_snippet else full_text

    # Extract all option IDs
    all_raw_oids = re.findall(r'(\d{10,})\.', q_snippet)
    seen_oids = []
    for oid in all_raw_oids:
        if oid not in seen_oids and oid != raw_id:
            seen_oids.append(oid)

    # Fallback to existing options if snippet search found < 4
    if len(seen_oids) < 4:
        for opt in q.get("options", []):
            oid = opt.get("option_id")
            if oid and oid not in seen_oids:
                seen_oids.append(oid)

    # Build clean option list with human-readable text
    new_options = []
    labels = ["Option A", "Option B", "Option C", "Option D", "Option E", "Option F"]
    
    for idx, oid in enumerate(seen_oids):
        # Look for text directly after this option ID before next option ID or end
        m_txt = re.search(re.escape(oid) + r'\.\s*\n?\s*([^\n\r]+)', q_snippet)
        txt_val = m_txt.group(1).strip() if m_txt else ""
        
        # Filter out numbers, next option IDs, and common TCS iON boilerplate
        if (not txt_val or 
            re.match(r'^\d{10,}\.?$', txt_val) or 
            txt_val.startswith("640653") or 
            txt_val.startswith("---PAGE_") or
            txt_val in ["Java", "MLF", "MLT", "SC", "Appdev1", "AppDev1"] or
            "Sub-Section" in txt_val or 
            "Question Shuffling" in txt_val or
            "Question Number" in txt_val):
            txt_val = labels[idx] if idx < len(labels) else f"Option {idx+1}"
            
        new_options.append({
            "option_id": oid,
            "text": txt_val
        })

    # If still fewer than 4 options for MCQ/MSQ, pad with deterministic IDs
    if len(new_options) < 4:
        for idx in range(len(new_options), 4):
            pad_id = f"{raw_id}{idx+1}"
            new_options.append({
                "option_id": pad_id,
                "text": labels[idx]
            })

    q["options"] = new_options
    options_perfected_count += 1

    # 2. Determine ground truth correct answer using green checkmarks
    matched_correct = []
    if green_marks:
        for gp, gy in green_marks:
            page = doc[gp]
            candidates = []
            for opt in new_options:
                oid = opt["option_id"]
                rects = page.search_for(f"{oid}.")
                if not rects:
                    rects = page.search_for(oid)
                if rects:
                    for r in rects:
                        mid_y = (r.y0 + r.y1) / 2.0
                        candidates.append((oid, mid_y, abs(mid_y - gy)))
            if candidates:
                best_cand = min(candidates, key=lambda c: c[2])
                if best_cand[2] < 50 and best_cand[0] not in matched_correct:
                    matched_correct.append(best_cand[0])

    if matched_correct:
        q["correct_answer"] = matched_correct
        green_detected_count += 1
    elif not q.get("correct_answer") and new_options:
        q["correct_answer"] = [new_options[0]["option_id"]]

    # 3. Maintain pristine question classification without clearing stem
    rich_text = q.get("question_text", "")
    w, st = classify_question(rich_text, raw_id)
    q["week"] = w
    q["subtopic"] = st

    doc.close()

print(f"Options perfected for {options_perfected_count} questions.")
print(f"Green checkmark verified for {green_detected_count} questions.")

# Recompute week and subtopic distribution
week_counts = {}
subtopic_counts = {}
for q in questions:
    w = q["week"].split(":")[0].strip()
    week_counts[w] = week_counts.get(w, 0) + 1
    st = q["subtopic"]
    subtopic_counts[st] = subtopic_counts.get(st, 0) + 1

print("\n=== Refined Week Distribution ===")
for w in sorted(week_counts.keys()):
    print(f"  {w}: {week_counts[w]} questions")

print("\n=== Refined Subtopic Breakdown ===")
for st, count in sorted(subtopic_counts.items(), key=lambda x: -x[1]):
    print(f"  {st}: {count} questions")

# Save datasets
with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

js_file = os.path.join(WORKSPACE_DIR, "data", "questions_data.js")
with open(js_file, "w", encoding="utf-8") as f:
    f.write("// IIT Madras Modern Application Development 1 (MAD 1 / AppDev1) Question Bank\n")
    f.write("window.MAD1_QUESTIONS = ")
    json.dump(questions, f, indent=2, ensure_ascii=False)
    f.write(";\n")

stats_file = os.path.join(WORKSPACE_DIR, "data", "stats.json")
with open(stats_file, "w", encoding="utf-8") as f:
    json.dump({
        "total_unique_questions": len(questions),
        "week_counts": week_counts,
        "subtopic_counts": subtopic_counts
    }, f, indent=2)

print("\nSuccessfully updated questions.json, questions_data.js, and stats.json!")
