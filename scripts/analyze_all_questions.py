import json
import os
import re

WORKSPACE_DIR = r"C:\Users\avesh\Desktop\mad1-pyq-jee-platform"
DATA_FILE = os.path.join(WORKSPACE_DIR, "data", "questions.json")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    questions = json.load(f)

print(f"Loaded {len(questions)} questions")

# Let's inspect the text of all questions to verify what topics they cover
week1_keywords = ["bandwidth", "latency", "propagation delay", "speed on cable", "cable breaks", "rtt", "round trip", 
                  "gbps", "mbps", "transmission delay", "ascii", "utf-8", "unicode", "character encoding", 
                  "status code", "http status", "idempotent", "safe method", "dns", "domain name", "client-server", 
                  "tcp", "udp", "ip address", "3000 km", "6000 km", "repeaters", "grammar check"]

week2_keywords = ["<form", "input type", "type=\"submit\"", "type=\"checkbox\"", "type=\"radio\"", "<select", "<textarea",
                  "<dl>", "<dt>", "<dd>", "box-sizing", "border-box", "content-box", "flexbox", "justify-content",
                  "specificity", "selector", "#highlight", "important", "cascade", "combinator", "p.highlight",
                  "<table>", "<tr>", "<td>", "<nav>", "<header>", "<footer>", "<article>", "<section>"]

week3_keywords = ["sys.argv", "command-line", "flask", "app = flask", "app.route", "@app.route", "methods=['get'", 
                  "methods=['post'", "request.args", "request.form", "request.values", "request.method", "url_for", 
                  "redirect", "abort(", "errorhandler", "render_template", "debug=true"]

week4_keywords = ["jinja", "template(", "string.template", "templatel", "template2", "{%", "{{", "loop.index", 
                  "macro", "{% macro", "{% extends", "{% block", "sqlite3", "connect(", "cursor", "execute(", 
                  "fetchall", "commit()", "create table", "foreign key", "primary key", "references"]

counts = {"Week 1": 0, "Week 2": 0, "Week 3": 0, "Week 4": 0, "Uncertain": 0}
uncertain_list = []

for q in questions:
    txt = (q.get("question_text", "") + " " + " ".join(o.get("text", "") for o in q.get("options", []))).lower()
    raw_id = str(q.get("raw_q_id", ""))
    
    # Week 1 checks
    is_w1 = any(k in txt for k in ["bandwidth", "latency", "propagation", "cable", "rtt", "round trip", "gbps", "mbps", 
                                   "ascii", "utf-8", "unicode", "status code", "3000 km", "6000 km", "repeaters", "grammar check",
                                   "client-server", "domain name", "ip address"])
    # Week 4 checks
    is_w4 = any(k in txt for k in ["jinja", "sqlite", "template2", "templatel", "macro", "loop.index", "create table", 
                                   "foreign key", "primary key", "{%", "{{", "fetchall"])
    # Week 3 checks
    is_w3 = any(k in txt for k in ["app.route", "request.args", "request.form", "sys.argv", "url_for", "redirect", "app = flask"])
    # Week 2 checks
    is_w2 = any(k in txt for k in ["<form", "input type", "<dl>", "<dt>", "specificity", "box-sizing", "border-box", 
                                   "flexbox", "selector", "#highlight", "stylesheet", "css"])
    
    current_w = q.get("week", "").split(":")[0]
    # print sample
    if q["id"] in ["MAD1_011", "MAD1_103", "MAD1_118", "MAD1_135", "MAD1_163"]:
        print(f"Target {q['id']} ({raw_id}): Current={current_w} | W1={is_w1}, W2={is_w2}, W3={is_w3}, W4={is_w4}")
