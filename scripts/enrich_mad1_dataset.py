import asyncio
import os
import re
import json
import glob
from PIL import Image
import winrt.windows.media.ocr as ocr
import winrt.windows.graphics.imaging as imaging
import winrt.windows.storage as storage

WORKSPACE_DIR = r"C:\Users\avesh\Desktop\mad1-pyq-jee-platform"
DATA_DIR = os.path.join(WORKSPACE_DIR, "data")
CARDS_DIR = os.path.join(WORKSPACE_DIR, "assets", "q_cards")

engine = ocr.OcrEngine.try_create_from_user_profile_languages()

async def ocr_image(full_path):
    norm_path = os.path.normpath(full_path)
    if not os.path.exists(norm_path):
        return ""
    try:
        f = await storage.StorageFile.get_file_from_path_async(norm_path)
        stream = await f.open_async(storage.FileAccessMode.READ)
        decoder = await imaging.BitmapDecoder.create_async(stream)
        bitmap = await decoder.get_software_bitmap_async()
        res = await engine.recognize_async(bitmap)
        return res.text
    except Exception as e:
        print(f"OCR Error on {os.path.basename(norm_path)}: {e}")
        return ""

def clean_ocr_text(raw_text):
    t = raw_text
    m = re.search(r'Question Label\s*:\s*(Multiple Choice Question|Multiple Select Question|Comprehension|Short Answer Question|Numerical Question|Text Question)\s*(.*)', t, flags=re.DOTALL | re.IGNORECASE)
    if m:
        t = m.group(2)
    else:
        m2 = re.search(r'Correct Marks\s*:\s*[0-9.]+\s*(.*)', t, flags=re.DOTALL | re.IGNORECASE)
        if m2:
            t = m2.group(1)
            
    t = re.split(r'Sub-Section Number\s*:', t, flags=re.IGNORECASE)[0]
    t = re.split(r'Question Number\s*:\s*\d+', t, flags=re.IGNORECASE)[0]
    t = re.sub(r'THIS IS QUESTION PAPER FOR THE SUBJECT.*', '', t, flags=re.DOTALL | re.IGNORECASE)
    t = re.sub(r'ARE YOU SURE YOU HAVE TO WRITE EXAM.*', '', t, flags=re.DOTALL | re.IGNORECASE)
    t = re.sub(r'CROSS CHECK YOUR HALL TICKET.*', '', t, flags=re.DOTALL | re.IGNORECASE)
    
    stem_part = t.split("Options :")[0] if "Options :" in t else t
    opts_part = t.split("Options :")[1] if "Options :" in t else ""
    
    clean_stem = re.sub(r'\s+', ' ', stem_part).strip()
    return clean_stem, opts_part.strip()

TAXONOMY = {
    "Week 1: Internet Architecture, HTTP & Network Calculations": [
        ("1.1 Web & Internet Basics (Client-Server Architecture, Protocols & Servers)", [
            "client-server", "client server", "web server", "dns", "domain name", "ip address", 
            "protocol", "tcp", "udp", "socket", "port", "architecture", "browser", "host", "packet", "layer"
        ]),
        ("1.2 Data Transmission, Bandwidth, RTT & Propagation Delay Calculations", [
            "bandwidth", "propagation delay", "transmission delay", "rtt", "round trip", "latency", 
            "throughput", "concurrent clients", "mbps", "kbps", "gbps", "bits per second", "bytes", 
            "data consumption", "packet size", "distance", "speed of light", "channel capacity", "motion calculations",
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
            "mime", "stateless", "http methods", "http request", "http response", "cookie", "session", "cache"
        ])
    ],
    "Week 2: HTML5, CSS3, Box Model & Form Controls": [
        ("2.1 HTML5 Elements, Semantic Tags & Document Structure", [
            "doctype", "html5", "semantic", "header", "footer", "nav", "article", "section", 
            "aside", "table", "tr", "td", "th", "ul", "ol", "li", "a href", "img src", "paragraph", 
            "heading", "dom", "tag", "element", "attribute", "alt", "title", "body", "head"
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
        ("3.1 Python for Web & Command-Line Arguments", [
            "sys.argv", "sys.argv[0]", "sys.argv[1]", "sys.argv[2]", "command-line", "command line", 
            "script argument", "len(sys.argv)", "import sys", "python web"
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

async def main():
    q_file = os.path.join(DATA_DIR, "questions.json")
    with open(q_file, "r", encoding="utf-8") as f:
        questions = json.load(f)
        
    print(f"Loaded {len(questions)} questions. Starting OCR processing...")
    
    # Process each card with WinRT OCR
    enriched_questions = []
    sem = asyncio.Semaphore(1)
    
    async def process_one(q, idx):
        async with sem:
            card_rel = q.get("card_image")
            if card_rel:
                full_card = os.path.join(WORKSPACE_DIR, card_rel.replace("/", os.sep))
                ocr_raw = await ocr_image(full_card)
                if ocr_raw:
                    stem, opts = clean_ocr_text(ocr_raw)
                    # If OCR text is longer and meaningful, update question_text
                    if len(stem) > len(q["question_text"]):
                        q["question_text"] = stem
                        
            # Reclassify based on enriched text
            full_text = f"{q.get('question_text', '')} {' '.join(o.get('text', '') for o in q.get('options', []))}"
            w, st = classify_question(full_text)
            q["week"] = w
            q["subtopic"] = st
            return q
            
    tasks = [process_one(q, i) for i, q in enumerate(questions)]
    enriched_questions = await asyncio.gather(*tasks)
    
    # Re-run strict deduplication on enriched text
    unique_map = {}
    fingerprint_map = {}
    for q in enriched_questions:
        norm_stem = re.sub(r'\s+', ' ', q["question_text"].lower()).strip()
        norm_key = re.sub(r'[^a-z0-9]', '', norm_stem)
        if len(norm_key) < 20:
            opt_str = "".join([re.sub(r'[^a-z0-9]', '', o.get("text", "").lower()) for o in q.get("options", [])])
            norm_key = f"short_{q['question_type']}_{opt_str}"
            if len(norm_key) < 15:
                norm_key = f"img_{q['marks']}_{q['raw_q_id']}"
                
        if norm_key in fingerprint_map:
            exist_id = fingerprint_map[norm_key]
            exist = unique_map[exist_id]
            for p in q.get("source_papers", []):
                if p not in exist["source_papers"]:
                    exist["source_papers"].append(p)
            if len(q.get("options", [])) > len(exist.get("options", [])):
                exist["options"] = q["options"]
            if len(q.get("question_text", "")) > len(exist.get("question_text", "")):
                exist["question_text"] = q["question_text"]
        else:
            fingerprint_map[norm_key] = q["id"]
            unique_map[q["id"]] = q
            
    final_questions = list(unique_map.values())
    
    # Renumber IDs sequentially
    for idx, q in enumerate(final_questions):
        q["id"] = f"MAD1_{idx+1:03d}"
        
    print(f"\nFinal Deduplicated Questions: {len(final_questions)}")
    
    # Recalculate statistics
    week_counts = {}
    subtopic_counts = {}
    for q in final_questions:
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
        
    # Save enriched datasets
    with open(q_file, "w", encoding="utf-8") as f:
        json.dump(final_questions, f, indent=2, ensure_ascii=False)
    print(f"\nSaved updated {q_file}")
    
    stats_file = os.path.join(DATA_DIR, "stats.json")
    stats = {
        "total_unique_questions": len(final_questions),
        "week_counts": week_counts,
        "subtopic_counts": subtopic_counts
    }
    with open(stats_file, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
        
    js_bundle_path = os.path.join(DATA_DIR, "questions_data.js")
    with open(js_bundle_path, "w", encoding="utf-8") as f:
        f.write("// IIT Madras Modern Application Development 1 (MAD 1 / AppDev1) Question Bank\n")
        f.write("window.MAD1_QUESTIONS = ")
        json.dump(final_questions, f, indent=2, ensure_ascii=False)
        f.write(";\n")
    print(f"Saved updated {js_bundle_path}")

if __name__ == "__main__":
    asyncio.run(main())
