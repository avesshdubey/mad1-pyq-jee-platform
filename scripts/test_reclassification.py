import json
import os
import re

WORKSPACE_DIR = r"C:\Users\avesh\Desktop\mad1-pyq-jee-platform"
DATA_FILE = os.path.join(WORKSPACE_DIR, "data", "questions.json")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    questions = json.load(f)

def classify_question(q):
    raw_id = str(q.get("raw_q_id", ""))
    txt = (q.get("question_text", "") + " " + " ".join(o.get("text", "") for o in q.get("options", []))).lower()
    
    # 1. Week 1: Network & Internet & HTTP
    # 1.2 Network Calculations
    if any(k in txt for k in ["bandwidth", "propagation delay", "speed on cable", "cable breaks", "3000 km", "6000 km", 
                              "round trip latency", "round trip", "rtt", "gbps", "mbps", "repeaters which added", "grammar checking"]):
        return "Week 1: Internet Architecture, HTTP & Network Calculations", "1.2 Data Transmission, Bandwidth, RTT & Propagation Delay Calculations"
    # 1.3 Character Encoding
    if any(k in txt for k in ["ascii", "utf-8", "unicode", "character encoding"]):
        return "Week 1: Internet Architecture, HTTP & Network Calculations", "1.3 Character Encoding & Representation (ASCII, Unicode, UTF-8 & Binary)"
    # 1.4 HTTP Protocol & Status Codes
    if any(k in txt for k in ["status code", "http status", "idempotent", "safe method", "http method", "request line", "http header", "user-agent", "301", "302", "404", "500"]):
        if not any(k in txt for k in ["render_template", "@app.route", "app = flask"]):
            return "Week 1: Internet Architecture, HTTP & Network Calculations", "1.4 HTTP Protocol, URLs, Request/Response Headers & Status Codes"
    # 1.1 Web & Internet Basics
    if any(k in txt for k in ["client-server", "dns", "domain name", "ip address", "socket", "port 80", "tcp", "udp"]) and not any(k in txt for k in ["flask", "jinja", "sqlite"]):
        return "Week 1: Internet Architecture, HTTP & Network Calculations", "1.1 Web & Internet Basics (Client-Server Architecture, Protocols & Servers)"
    
    # 2. Week 4: Jinja2, SQLite & Databases
    # 4.3 & 4.4 SQLite & Relational
    if any(k in txt for k in ["sqlite3", "connect(", "cursor.execute", "cursor =", "fetchall", "fetchone", "conn.commit"]):
        return "Week 4: Jinja2 Templating, Dynamic Rendering, SQLite & CRUD Applications", "4.4 Database Integration in Flask (sqlite3, Cursor & Connection)"
    if any(k in txt for k in ["create table", "foreign key", "primary key", "references", "cascade", "database schema"]):
        return "Week 4: Jinja2 Templating, Dynamic Rendering, SQLite & CRUD Applications", "4.3 SQLite & Relational Data Modeling (Schema, Tables, Types, Primary & Foreign Keys)"
    # 4.2 Jinja2 Filters, Macros & Template Inheritance
    if any(k in txt for k in ["{% macro", "macro greet", "{% extends", "{% block", "template inheritance", "| upper", "| lower", "| default"]):
        return "Week 4: Jinja2 Templating, Dynamic Rendering, SQLite & CRUD Applications", "4.2 Jinja2 Filters, Macros & Template Inheritance"
    # 4.1 Jinja2 Templating Basics
    if any(k in txt for k in ["jinja", "jinja_template", "string_template", "templatel", "template2", "loop.index", "{%", "{{", "endfor", "endif", "index.html"]):
        if not any(k in txt for k in ["@app.route", "request.form"]):
            return "Week 4: Jinja2 Templating, Dynamic Rendering, SQLite & CRUD Applications", "4.1 Jinja2 Templating Basics (Variables & Control Flow)"
    
    # 3. Week 3: Backend Python & Flask
    # 3.1 Command-Line
    if any(k in txt for k in ["sys.argv", "import sys", "command-line", "command line arguments"]):
        return "Week 3: Backend Python, Flask Essentials, Routing & Request Handling", "3.1 Python Web Fundamentals & Command-Line Arguments"
    # 3.5 Flask Responses, Redirects & Error Handling
    if any(k in txt for k in ["redirect(", "url_for(", "abort(", "@app.errorhandler"]):
        return "Week 3: Backend Python, Flask Essentials, Routing & Request Handling", "3.6 Flask Responses, Redirects & Error Handling"
    # 3.4 Flask Request Object
    if any(k in txt for k in ["request.args", "request.form", "request.values", "request.method", "request.get_json"]):
        return "Week 3: Backend Python, Flask Essentials, Routing & Request Handling", "3.5 Flask Request Object & Data Extraction"
    # 3.3 Flask Routing
    if any(k in txt for k in ["@app.route", "app.route", "<int:", "<string:", "methods=['get'"]):
        return "Week 3: Backend Python, Flask Essentials, Routing & Request Handling", "3.3 Routing, Dynamic URL Converters & View Functions"
    # 3.2 Flask App Setup / MVC
    if any(k in txt for k in ["flask", "app = flask", "app.run", "debug=true", "mvc architecture", "model information to view"]):
        return "Week 3: Backend Python, Flask Essentials, Routing & Request Handling", "3.2 Flask Application Setup & App Configuration"
    
    # 4. Week 2: HTML5 & CSS3
    # 2.3 CSS Selectors & Specificity
    if any(k in txt for k in ["specificity", "selector", "#highlight", "important", "cascade", "combinator", "p.highlight", "pseudo-class"]):
        return "Week 2: HTML5, CSS3, Box Model & Form Controls", "2.3 CSS Selectors, Specificity & Cascade Rules"
    # 2.4 CSS Box Model & Layout
    if any(k in txt for k in ["box-sizing", "border-box", "content-box", "flexbox", "display: flex", "justify-content", "align-items", "position: absolute", "position: relative", "margin", "padding"]):
        return "Week 2: HTML5, CSS3, Box Model & Form Controls", "2.4 CSS Box Model & Layouts (Flexbox, Positioning & Spacing)"
    # 2.2 HTML Forms
    if any(k in txt for k in ["<form", "input type", "type=\"submit\"", "type=\"checkbox\"", "type=\"radio\"", "<select", "<textarea", "action=", "form submission"]):
        return "Week 2: HTML5, CSS3, Box Model & Form Controls", "2.2 HTML Forms, Input Types, Attributes & Form Submission"
    # 2.1 HTML5 Elements & Structure
    if any(k in txt for k in ["<dl>", "<dt>", "<dd>", "<header>", "<nav>", "<article>", "<section>", "<footer>", "<table>", "<tr>", "<td>", "doctype html", "<html>"]):
        return "Week 2: HTML5, CSS3, Box Model & Form Controls", "2.1 HTML5 Elements, Semantic Tags & Document Structure"
        
    # Fallback to existing
    return q.get("week"), q.get("subtopic")

from collections import Counter
new_weeks = []
new_subtopics = []
changed = 0

for q in questions:
    old_w = q.get("week")
    old_s = q.get("subtopic")
    w, s = classify_question(q)
    new_weeks.append(w.split(":")[0])
    new_subtopics.append(s)
    if w != old_w or s != old_s:
        changed += 1

print(f"Total reclassified: {changed} / {len(questions)}")
print("New Week distribution:", Counter(new_weeks))
print("New Subtopic distribution:")
for st, cnt in Counter(new_subtopics).most_common():
    print(f"  {cnt:3d}: {st}")
