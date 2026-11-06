import json
import os
import re
from collections import Counter

WORKSPACE_DIR = r"C:\Users\avesh\Desktop\mad1-pyq-jee-platform"
DATA_FILE = os.path.join(WORKSPACE_DIR, "data", "questions.json")
JS_DATA_FILE = os.path.join(WORKSPACE_DIR, "data", "questions_data.js")
STATS_FILE = os.path.join(WORKSPACE_DIR, "data", "stats.json")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    questions = json.load(f)

print(f"Loaded {len(questions)} questions from {DATA_FILE}")

def clean_stem(raw_text):
    parts = raw_text.split("Options :")
    stem = parts[0]
    m = re.search(r'[A-Za-z!):]+uestion\s+Label\s*:\s*[A-Za-z ]*\n?(.*)', stem, flags=re.DOTALL | re.IGNORECASE)
    if m:
        c = m.group(1).strip()
    else:
        c = stem.strip()
    c = re.sub(r'^[ :]+', '', c)
    return c

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
    # 4.4 Database Integration in Flask
    if any(k in txt for k in ["sqlite3", "connect(", "cursor.execute", "cursor =", "fetchall", "fetchone", "conn.commit"]):
        return "Week 4: Jinja2 Templating, Dynamic Rendering, SQLite & CRUD Applications", "4.4 Database Integration in Flask (sqlite3, Cursor & Connection)"
    # 4.3 SQLite & Relational Data Modeling
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
        return "Week 3: Backend Python, Flask Essentials, Routing & Request Handling", "3.5 Flask Responses, Redirects & Error Handling"
    # 3.4 Flask Request Object
    if any(k in txt for k in ["request.args", "request.form", "request.values", "request.method", "request.get_json"]):
        return "Week 3: Backend Python, Flask Essentials, Routing & Request Handling", "3.4 Flask Request Object & Data Extraction"
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
        
    return q.get("week"), q.get("subtopic")

def generate_explanation(q, week, subtopic):
    raw_id = str(q.get("raw_q_id", ""))
    q_type = q.get("question_type", "MCQ")
    options = q.get("options", [])
    correct_ids = [str(x) for x in q.get("correct_answer", [])]
    raw_txt = q.get("question_text", "")
    stem = clean_stem(raw_txt)
    txt_lower = (raw_txt + " " + " ".join(o.get("text", "") for o in options)).lower()
    
    opt_ids = [str(o.get("option_id")) for o in options]
    correct_letters = []
    correct_texts = []
    
    if q_type == "SA":
        correct_label = f"Value: {correct_ids[0] if correct_ids else 'N/A'}"
        correct_text = correct_ids[0] if correct_ids else ""
    else:
        for cid in correct_ids:
            if cid in opt_ids:
                idx = opt_ids.index(cid)
                letter = chr(65 + idx)
                correct_letters.append(letter)
                otext = options[idx].get("text", "")
                if otext and not otext.startswith("Option ") and not otext.startswith("640653"):
                    correct_texts.append(otext)
                else:
                    correct_texts.append(f"Option {letter}")
        if len(correct_letters) == 1:
            correct_label = f"Option {correct_letters[0]}"
        elif len(correct_letters) > 1:
            correct_label = "Options " + ", ".join(correct_letters)
        else:
            correct_label = "Option A"
        correct_text = " | ".join(correct_texts) if correct_texts else correct_label

    # Specific Question Explanations
    # 1. Network Propagation Calculation: 3000 km, cable 2e8 m/s, air 3e8 m/s, server delay 47 ms -> 72 ms
    if "3000 km" in txt_lower or raw_id in ["6406531298443", "6406531297903", "6406531298173"]:
        correct_label = "Value: 72"
        correct_text = "72 ms"
        step_by_step = [
            "Step 1: Calculate request propagation delay through cable: Distance = 3000 km = 3 × 10^6 m, Speed in cable = 2 × 10^8 m/s. Delay = (3 × 10^6) / (2 × 10^8) = 0.015 s = 15 ms.",
            "Step 2: Add server-side medium change delay: Additional delay at server end = 47 ms.",
            "Step 3: Calculate response propagation delay through air: Distance = 3000 km = 3 × 10^6 m, Speed in air = 3 × 10^8 m/s. Delay = (3 × 10^6) / (3 × 10^8) = 0.010 s = 10 ms.",
            "Step 4: Total waiting time for client = Request delay + Server delay + Response delay = 15 ms + 47 ms + 10 ms = 72 ms."
        ]
        concept = "Network Latency & Propagation Delay: Total Latency = T_prop(request) + T_processing + T_prop(response), where T_prop = Distance / Propagation_Speed."
        exam_trick = "Convert distance directly to km/s: Cable speed = 200,000 km/s -> 3000/200,000 = 15 ms. Air speed = 300,000 km/s -> 3000/300,000 = 10 ms. Total = 15 + 47 + 10 = 72 ms! (Solved in 5 seconds)."
        trap_alert = "Forgetting to include the server processing delay of 47 ms, or assuming cable speed equals speed of light in vacuum (3e8 m/s)."

    # 1b. Network Propagation: 6000 km, repeater delay 75 ms -> 125 ms (MAD1_027)
    elif "6000 kilometer" in txt_lower or raw_id == "640653345256":
        correct_label = "Option C"
        correct_text = "125 milliseconds"
        step_by_step = [
            "Step 1: Request propagation delay through cable: Distance = 6000 km = 6 × 10^6 m, Speed in cable = 2 × 10^8 m/s. Delay = (6 × 10^6) / (2 × 10^8) = 0.030 s = 30 ms.",
            "Step 2: Repeater hardware delay: Given as 75 ms.",
            "Step 3: Response propagation delay through air: Distance = 6000 km = 6 × 10^6 m, Speed in air = 3 × 10^8 m/s. Delay = (6 × 10^6) / (3 × 10^8) = 0.020 s = 20 ms.",
            "Step 4: Total waiting time for client = 30 ms + 75 ms + 20 ms = 125 ms (Option C)."
        ]
        concept = "Network Delay Composition: Round-Trip Latency = Cable Delay + Repeater Processing Delay + Air Delay."
        exam_trick = "Calculate in km/s: Cable: 6000 / 200,000 = 30 ms. Air: 6000 / 300,000 = 20 ms. Sum = 30 + 75 + 20 = 125 ms! Solved in 5 seconds."
        trap_alert = "Forgetting the 75 ms repeater delay or assuming signal speed in cable equals speed of light in vacuum."

    # 1c. Bandwidth Scaling: 4000 req/sec with +6 Kb -> 24 Mbps (MAD1_039)
    elif ("4000 request" in txt_lower and "6 kb" in txt_lower) or raw_id == "640653737406":
        correct_label = "Option B"
        correct_text = "24 Mbps"
        step_by_step = [
            "Step 1: The question asks specifically for the *additional* bandwidth required, not the total bandwidth.",
            "Step 2: Rate of requests = 4000 requests per second.",
            "Step 3: Additional data per request = 6 Kb (kilobits).",
            "Step 4: Additional throughput = 4000 requests/sec × 6 Kb = 24,000 Kbps.",
            "Step 5: Convert Kbps to Mbps: 24,000 Kbps / 1000 = 24 Mbps (Option B)."
        ]
        concept = "Network Throughput Scaling: Additional Bandwidth = Request Frequency × Incremental Payload Size."
        exam_trick = "Mental math: 4000 * 6 Kb = 24,000 Kbps = 24 Mbps! Takes 2 seconds."
        trap_alert = "Adding the existing 12 Mbps to get total bandwidth (36 Mbps) when the prompt asks strictly for the additional bandwidth required."

    # 1d. Network Latency: Nodes A to B, B to C, C to D -> 265 ms (MAD1_134, raw 640653825027)
    elif raw_id == "640653825027" or ("datacenter c" in txt_lower and "datacenter d" in txt_lower and "round trip latency" in txt_lower):
        correct_label = "Option C"
        correct_text = "265"
        step_by_step = [
            "Step 1: Calculate one-way propagation delays across each network segment:\n  - Link A to B: Distance = 12,000 km, Speed = 3 × 10^8 m/s = 300,000 km/s -> Delay = 12,000 / 300,000 = 0.040 s = 40 ms.\n  - Link B to C: Distance = 8,500 km, Speed = 2 × 10^8 m/s = 200,000 km/s -> Delay = 8,500 / 200,000 = 0.0425 s = 42.5 ms.\n  - Link C to D: Distance = 7,500 km, Speed = 1.5 × 10^8 m/s = 150,000 km/s -> Delay = 7,500 / 150,000 = 0.050 s = 50 ms.",
            "Step 2: Sum the one-way delays from client A through B and C to datacenter D: 40 ms + 42.5 ms + 50 ms = 132.5 ms.",
            "Step 3: Calculate full Round-Trip Time (RTT): The return path traverses the reverse route, doubling the propagation delay: 2 × 132.5 ms = 265 ms.",
            "Step 4: Confirm Option C (265) matches the exact question requirement."
        ]
        concept = "Multi-Hop Network Latency & Round-Trip Time: RTT = 2 × ∑(Distance_i / Speed_i) across all constituent physical links."
        exam_trick = "Convert speed to km/s: 3e8 = 300,000 km/s; 2e8 = 200,000 km/s; 1.5e8 = 150,000 km/s. One-way = 40 + 42.5 + 50 = 132.5 ms. Round-trip = 265 ms! Solved in 10 seconds."
        trap_alert = "Selecting Option B (132.5 ms) by reporting one-way delay instead of round-trip latency."

    # 1e. MVC Architecture: Controller passes data model to view (MAD1_017)
    elif ("mvc architecture" in txt_lower or raw_id == "640653345241") and "model information to view" in txt_lower:
        correct_label = "Option C"
        correct_text = "The controller passes data model information to view."
        step_by_step = [
            "Step 1: In the Model-View-Controller (MVC) architectural design pattern, the Controller acts as the orchestrator between data and presentation.",
            "Step 2: The Controller receives the incoming HTTP request from the client, queries or updates the Model, and passes the resulting data model objects to the View for rendering.",
            "Step 3: The View never directly redirects requests to the Model (ruling out Option A).",
            "Step 4: Views can be reused across multiple controllers (ruling out Option D).",
            "Step 5: Therefore, Option C ('The controller passes data model information to view') is the correct statement."
        ]
        concept = "MVC (Model-View-Controller) Architecture: Clean separation of concerns where Controller mediates all communication between the Model (data state) and the View (UI presentation)."
        exam_trick = "In MVC, Controller is the middleman: Request -> Controller -> Model -> Controller -> View -> User!"
        trap_alert = "Believing that the View directly queries or updates the Model without Controller mediation."

    # 1f. Flask Protein Intake Route (MAD1_015)
    elif "recommended daily protein intake" in txt_lower or raw_id == "6406531298449":
        correct_label = "Option B"
        correct_text = "Recommended Daily Protein Intake | Gender: FeMaLe weight: 154lb | Recommended Intake: 52 grams"
        step_by_step = [
            "Step 1: Inspect the Flask view function: query parameters or test cases pass `gender='FeMaLe'` and weight in pounds `weight=154lb`.",
            "Step 2: Convert body weight to kilograms: 154 lb / 2.2 ≈ 70 kg.",
            "Step 3: Apply the recommended dietary intake coefficient for women (~0.74–0.8 g/kg): 70 kg × 0.74 ≈ 52 grams.",
            "Step 4: The Jinja2 template outputs the formatted variables matching Option B."
        ]
        concept = "Flask Request Context & Jinja2 Template Interpolation: Parsing URL query parameters, executing business logic calculations, and rendering formatted HTML output."
        exam_trick = "Match input parameters: Gender 'FeMaLe' with 154 lb corresponds to 52 grams of protein."
        trap_alert = "Picking the male calculation option (48g or higher ratio) by misreading the gender parameter."

    # 2. Network Bandwidth Calculation: 2 Gbps -> 250 MB
    elif "grammar checking" in txt_lower or "2 gbps" in txt_lower or raw_id == "6406531298442" or ("bandwidth" in txt_lower and "250" in correct_ids):
        correct_label = "Value: 250"
        correct_text = "250 MB"
        step_by_step = [
            "Step 1: Network bandwidth capacity is given as 2 Gbps (gigabits per second).",
            "Step 2: The question asks for transmission volume in MB (Megabytes) per second.",
            "Step 3: Recall binary/networking conversion: 8 bits = 1 Byte.",
            "Step 4: 2 Gbps = 2000 Mbps (or 2 × 10^9 bits/sec).",
            "Step 5: Convert megabits to Megabytes: 2000 Mbps / 8 = 250 MB/s. Hence, the numerical value is 250."
        ]
        concept = "Bandwidth Unit Conversion: 1 Byte = 8 bits. Always divide gigabits or megabits by 8 when converting to gigabytes or megabytes."
        exam_trick = "Fast conversion: Gbps to MB/s -> Multiply Gbps by 1000 and divide by 8: (2 * 1000) / 8 = 250 MB!"
        trap_alert = "Forgetting to divide by 8 and reporting 2000 MB instead of 250 MB."

    # 3. HTML Description List (<dl>, <dt>, <dd>)
    elif "<dl>" in txt_lower or raw_id == "6406531298433":
        correct_label = "Option A"
        step_by_step = [
            "Step 1: The `<dl>` element defines a Description/Definition List in HTML5.",
            "Step 2: `<dt>` defines the description term, rendered flush left without indentation.",
            "Step 3: `<dd>` defines the description details, rendered indented below the corresponding `<dt>`.",
            "Step 4: Unlike `<ul>` or `<ol>`, `<dl>` generates NO bullet points or numbers.",
            "Step 5: Therefore, 'Flask' and 'SQLAlchemy' appear flush left, while their descriptions are indented beneath them."
        ]
        concept = "HTML5 Description Lists (`<dl>`, `<dt>`, `<dd>`): Semantic structure for key-value pairs, glossaries, and metadata catalogs."
        exam_trick = "Mnemonic: DT = Direct Term (no indent), DD = Detailed Data (indented). Never has bullets (-)."
        trap_alert = "Selecting options that display bullet points or options where `<dd>` text is not indented."

    # 4. Jinja2 Macro Definition
    elif "macro greet" in txt_lower or raw_id == "6406531298437":
        correct_label = "Option A"
        step_by_step = [
            "Step 1: The template defines a Jinja2 macro: `{% macro greet(name) %} Hello, {{ name }}! {% endmacro %}`.",
            "Step 2: Macros in Jinja2 act like reusable Python functions inside templates.",
            "Step 3: Calling `{{ greet('Alice') }}` renders `Hello, Alice!`.",
            "Step 4: Calling `{{ greet('Bob') }}` renders `Hello, Bob!`.",
            "Step 5: Both calls output their rendered text into the template stream sequentially."
        ]
        concept = "Jinja2 Macro Definition & Invocation: `{% macro name(args) %} ... {% endmacro %}` creates modular reusable presentation components."
        exam_trick = "Macros execute in place and return evaluated strings. No exception is thrown for standard macro calls."
        trap_alert = "Thinking macros require a special `import` when declared in the same template file."

    # 5. CSS Specificity
    elif (".important" in txt_lower and "#highlight" in txt_lower) or raw_id == "6406531298439":
        correct_label = "Option B"
        correct_text = "Green"
        step_by_step = [
            "Step 1: Inspect the competing CSS rules targeting the `<p>` element:\n  - Element selector `p`: Specificity = (0, 0, 1)\n  - Class selector `.important`: Specificity = (0, 1, 0)\n  - ID selector `#highlight`: Specificity = (1, 0, 0).",
            "Step 2: Compare specificities from left to right: (1, 0, 0) > (0, 1, 0) > (0, 0, 1).",
            "Step 3: The ID selector `#highlight` has the highest specificity (1 ID vs 0 IDs).",
            "Step 4: Therefore, the color defined by `#highlight` ('green') wins, regardless of order in the stylesheet."
        ]
        concept = "CSS Specificity Hierarchy: Inline styles (1,0,0,0) > ID selectors (0,1,0,0) > Class/Attribute/Pseudo-class selectors (0,0,1,0) > Element selectors (0,0,0,1)."
        exam_trick = "Rule of thumb: Count IDs first. Any rule with an ID beats any number of classes without `!important`."
        trap_alert = "Assuming `.important` wins because of its class name — it is merely a normal class name, NOT the `!important` directive!"

    # 6. General Subtopic-Based Explanations
    elif subtopic.startswith("1.1"):
        step_by_step = [
            "Step 1: Analyze the client-server architecture model and internet protocols (DNS, TCP, IP, HTTP).",
            "Step 2: DNS translates human-readable domain names into routable numerical IP addresses.",
            "Step 3: TCP provides reliable, ordered byte-stream delivery with 3-way handshakes, while UDP offers lightweight connectionless transmission.",
            "Step 4: Select the statement that accurately captures core internet infrastructure operation."
        ]
        concept = "Web & Internet Architectural Foundations: Client-server interaction, name resolution (DNS), and transport-layer abstractions."
        exam_trick = "DNS = Name-to-IP directory; TCP = Reliable connection; Port 80 = Standard HTTP; Port 443 = HTTPS."
        trap_alert = "Confusing application layer protocols (HTTP, DNS) with transport layer protocols (TCP, UDP)."

    elif subtopic.startswith("1.2"):
        step_by_step = [
            "Step 1: Identify given network parameters: Distance, link propagation speed, packet size, and bandwidth capacity.",
            "Step 2: Apply the governing delay equations:\n  - Propagation Delay: T_prop = Distance / Propagation_Speed\n  - Transmission Delay: T_trans = Packet_Size / Bandwidth\n  - RTT (Round Trip Time): 2 × T_prop + Queuing/Processing Delays.",
            "Step 3: Convert units accurately (1 Byte = 8 bits, 1 km = 1,000 m, 1 ms = 10^-3 s, 1 Gbps = 10^9 bps).",
            "Step 4: Substitute the values to verify the numerical or conceptual match in the official key."
        ]
        concept = "Network Transmission Fundamentals: Propagation delay is strictly independent of packet size (governed by distance/medium); Transmission delay is determined by packet size divided by channel bandwidth."
        exam_trick = "Check what is changing: Double the distance? Propagation delay doubles. Double the packet size? Only transmission delay doubles!"
        trap_alert = "Failing to convert bits to Bytes when comparing transmission rates with file sizes."

    elif subtopic.startswith("1.3"):
        step_by_step = [
            "Step 1: Identify character encoding standard: Standard ASCII (7 bits, 128 characters), Extended ASCII (8 bits, 256 characters), Unicode (code points U+0000 to U+10FFFF), UTF-8 (variable 1 to 4 bytes).",
            "Step 2: Evaluate code point values: standard English characters (0-127) encode into exactly 1 byte in UTF-8.",
            "Step 3: Verify binary length and backward-compatibility rules.",
            "Step 4: Conclude which statement aligns with character representation architecture."
        ]
        concept = "Character Representation Architecture: UTF-8 provides universal character representation while maintaining 100% binary backward compatibility with standard 7-bit ASCII."
        exam_trick = "Standard ASCII code points (0-127) take 1 byte in UTF-8. UTF-8 is self-synchronizing and variable-length."
        trap_alert = "Believing that UTF-8 always uses 8 bits for all characters globally."

    elif subtopic.startswith("1.4"):
        step_by_step = [
            "Step 1: Inspect the HTTP method (GET, POST, PUT, DELETE, PATCH, HEAD) or status code (2xx, 3xx, 4xx, 5xx) evaluated.",
            "Step 2: Check safety and idempotence definitions:\n  - Safe methods (do not alter server state): GET, HEAD, OPTIONS\n  - Idempotent methods (multiple identical requests produce same server state): GET, PUT, DELETE, HEAD, OPTIONS\n  - Non-idempotent methods: POST, PATCH.",
            "Step 3: Evaluate response codes: 200 (OK), 201 (Created), 301 (Moved Permanently), 302 (Found/Temporary Redirect), 400 (Bad Request), 404 (Not Found), 500 (Internal Server Error).",
            "Step 4: Correlate the prompt requirements with HTTP protocol specifications to confirm the correct choice."
        ]
        concept = "HTTP Method Semantics & Idempotency: Essential for RESTful API design and reliable client-server communication."
        exam_trick = "GET, PUT, DELETE = Idempotent (running 1 time or 100 times has same end state). POST = NOT idempotent (creates duplicate records)."
        trap_alert = "Confusing 301 (Permanent redirect, cached by browser) with 302 (Temporary redirect, not cached by default)."

    elif subtopic.startswith("2.1"):
        step_by_step = [
            "Step 1: Examine the HTML5 markup structure and tags (`<header>`, `<nav>`, `<article>`, `<section>`, `<footer>`, `<dl>`, `<table>`).",
            "Step 2: HTML5 semantic tags communicate document meaning to browsers, screen readers, and search engine crawlers without altering visual appearance by default.",
            "Step 3: Verify parent-child nesting rules (e.g. `<dt>` and `<dd>` must be inside `<dl>`; `<tr>` inside `<table>`, `<tbody>`, etc.).",
            "Step 4: Determine the valid output or layout structure matching the specification."
        ]
        concept = "HTML5 Document Structure & Semantic Elements: Enhances accessibility, SEO, and structural clarity across web applications."
        exam_trick = "Semantic tags like `<section>` and `<article>` behave visually as generic block elements (`display: block`) by default."
        trap_alert = "Assuming HTML5 semantic elements apply special decorative styling automatically."

    elif subtopic.startswith("2.2"):
        step_by_step = [
            "Step 1: Inspect form control types and attributes (`action`, `method`, `name`, `value`, `required`, `disabled`).",
            "Step 2: Remember that inputs without a `name` attribute will NEVER submit their data to the server upon form submission.",
            "Step 3: In GET forms, form values are appended to the URL query string; in POST forms, data is transmitted in the HTTP request payload body.",
            "Step 4: Radio buttons with the SAME `name` attribute form a mutually-exclusive group; checkboxes allow multiple selections."
        ]
        concept = "HTML Form Controls & Data Serialization: Form elements encode user input into key-value pairs (`name=value`) sent via HTTP requests."
        exam_trick = "Radio buttons MUST share the exact same `name` attribute to allow only one selection at a time!"
        trap_alert = "Using the `id` attribute instead of the `name` attribute in form inputs when expecting backend form processing."

    elif subtopic.startswith("2.3"):
        step_by_step = [
            "Step 1: Deconstruct competing selectors into specificity tuples: (Inline, IDs, Classes/Attributes/Pseudo-classes, Elements/Pseudo-elements).",
            "Step 2: Compare from left to right: (1, 0, 0, 0) > (0, 1, 0, 0) > (0, 0, 1, 0) > (0, 0, 0, 1).",
            "Step 3: An ID selector always overrules any number of class selectors.",
            "Step 4: If specificities are equal, the rule defined later in the stylesheet wins."
        ]
        concept = "CSS Specificity Cascade Hierarchy: Precision determines rule precedence, with source order serving solely as a tie-breaker."
        exam_trick = "Count IDs (#) first. If one has an ID and others do not, it wins instantly without further calculation."
        trap_alert = "Assuming a higher class count can defeat an ID selector — specificity levels never carry over."

    elif subtopic.startswith("2.4"):
        step_by_step = [
            "Step 1: Identify the box model layout mode (`content-box` default vs `border-box`).",
            "Step 2: With `box-sizing: content-box`: Total Rendered Width = width + padding-left + padding-right + border-left + border-right.",
            "Step 3: With `box-sizing: border-box`: Declared width is inclusive of padding and borders.",
            "Step 4: In Flexbox: `justify-content` aligns items along the MAIN axis, while `align-items` aligns along the CROSS axis."
        ]
        concept = "CSS Layout Mechanics & Box Sizing: Controlling dimensions and alignments across standard and flexible container contexts."
        exam_trick = "`border-box` prevents layouts from breaking by absorbing padding/border into the set width. `justify-content` = main axis, `align-items` = cross axis."
        trap_alert = "Forgetting that margin is NEVER included inside `box-sizing: border-box`."

    elif subtopic.startswith("3.1"):
        step_by_step = [
            "Step 1: In Python, `sys.argv` stores command-line arguments as a list of strings.",
            "Step 2: `sys.argv[0]` is ALWAYS the script name itself.",
            "Step 3: Additional arguments passed on the terminal begin at `sys.argv[1]`.",
            "Step 4: Remember all elements in `sys.argv` are of type `str`; integer operations require explicit casting `int(sys.argv[i])`."
        ]
        concept = "Python Command-Line Interface (`sys.argv`): Capturing terminal parameters to configure server execution and scripts."
        exam_trick = "Remember length offset: `python script.py a b` -> `len(sys.argv) == 3`, `sys.argv[0] == 'script.py'`."
        trap_alert = "IndexError: Accessing `sys.argv[1]` when no command line arguments were provided."

    elif subtopic.startswith("3.2"):
        step_by_step = [
            "Step 1: Analyze Flask app initialization: `app = Flask(__name__)`.",
            "Step 2: In MVC architecture: Model = data/business logic; View = presentation layer (HTML/Jinja2); Controller = Flask route handler coordinating requests.",
            "Step 3: Running `app.run(debug=True)` activates the interactive debugger and auto-reloader (should NEVER be used in production).",
            "Step 4: Verify the application configuration and execution entry point."
        ]
        concept = "Flask Application Architecture & MVC: Clean separation between data model, view templates, and routing controllers."
        exam_trick = "Flask is a WSGI microframework. `__name__` helps Flask locate static files and templates relative to the module."
        trap_alert = "Leaving `debug=True` on in production environments, exposing arbitrary code execution via the web console."

    elif subtopic.startswith("3.3"):
        step_by_step = [
            "Step 1: Check endpoint path and converters in `@app.route()`: `<string>` (default), `<int>`, `<float>`, `<path>`.",
            "Step 2: Confirm function arguments match URL parameters defined in the route pattern.",
            "Step 3: Inspect HTTP methods: default is `['GET']`; `methods=['GET', 'POST']` is required for forms handling both.",
            "Step 4: Determine return value: string, HTML from `render_template`, redirect response, or tuple `(body, status_code)`."
        ]
        concept = "Flask URL Routing Architecture: Decorators bind URL routes to Python callable functions with automated parameter parsing."
        exam_trick = "Submitting a POST request to a route with default `@app.route('/...')` triggers HTTP `405 Method Not Allowed`."
        trap_alert = "Omitting type converters when expecting integer parameters (Flask defaults to string)."

    elif subtopic.startswith("3.4"):
        step_by_step = [
            "Step 1: Determine the HTTP method and data source.",
            "Step 2: In Flask:\n  - `request.args`: Query string parameters (e.g. `?name=val` in GET)\n  - `request.form`: MultiDict of form payload fields submitted in POST\n  - `request.get_json()`: Parsed JSON payload\n  - `request.method`: String representing request verb ('GET', 'POST').",
            "Step 3: Using bracket indexing `request.form['key']` raises `400 Bad Request` if key is absent; `request.form.get('key')` returns `None` safely.",
            "Step 4: Select the corresponding option."
        ]
        concept = "Flask Request Context & Payload Parsing: Granular isolation between query parameters and form body data."
        exam_trick = "Remember: `args` for URL queries (GET), `form` for HTML form bodies (POST)!"
        trap_alert = "Using `request.args` to inspect POST form submissions."

    elif subtopic.startswith("3.5"):
        step_by_step = [
            "Step 1: `url_for('function_name', **values)` generates the endpoint URL by referencing the Python view function name.",
            "Step 2: `redirect(target_url)` instructs the client browser to navigate to a new location with an HTTP 302 redirect.",
            "Step 3: Custom error pages use `@app.errorhandler(404)` returning a template and the explicit 404 status code.",
            "Step 4: Validate function arguments and return types."
        ]
        concept = "Flask Redirection & Dynamic URL Resolution: Decouples URL path layout from application logic."
        exam_trick = "`url_for` requires the Python function name as a string, NOT the URL route!"
        trap_alert = "Passing `/login` instead of `'login'` into `url_for`."

    elif subtopic.startswith("4.1"):
        step_by_step = [
            "Step 1: Recognize Jinja2 delimiters: `{{ ... }}` for variable output expressions, `{% ... %}` for control flow tags.",
            "Step 2: In loops: `{% for item in list %}` requires matching closing tag `{% endfor %}`.",
            "Step 3: Special loop helpers: `loop.index` (1, 2, 3...), `loop.index0` (0, 1, 2...), `loop.first` (boolean), `loop.last` (boolean).",
            "Step 4: Undefined variables render as empty strings by default without throwing errors."
        ]
        concept = "Jinja2 Dynamic Template Rendering: Powerful expression interpolation and programmatic template flow."
        exam_trick = "`loop.index` is 1-based; `loop.index0` is 0-based. `{{ }}` prints, `{% %}` executes!"
        trap_alert = "Forgetting `{% endfor %}` or `{% endif %}` closing tags in Jinja2 templates."

    elif subtopic.startswith("4.2"):
        step_by_step = [
            "Step 1: Macros define reusable UI fragments: `{% macro name(params) %} ... {% endmacro %}`.",
            "Step 2: Template inheritance: child templates use `{% extends 'base.html' %}` and override `{% block content %} ... {% endblock %}`.",
            "Step 3: Filters: `{{ var | upper }}`, `{{ var | length }}`, `{{ var | default('val') }}`.",
            "Step 4: Confirm block replacement and filter evaluation."
        ]
        concept = "Jinja2 Modularity: Macros, template inheritance, and filters maximize code reuse across views."
        exam_trick = "`extends` must always be the very first tag in a child template!"
        trap_alert = "Placing HTML content outside of `{% block %}` tags in a template that extends a base template."

    elif subtopic.startswith("4.3") or subtopic.startswith("4.4"):
        step_by_step = [
            "Step 1: Inspect SQLite relational constraints: `PRIMARY KEY` enforces uniqueness and non-null; `FOREIGN KEY` enforces referential integrity.",
            "Step 2: In Python `sqlite3`: queries use parameter placeholders `?` (`cursor.execute('SELECT * FROM t WHERE id=?', (val,))`) to prevent SQL injection.",
            "Step 3: DML operations (INSERT, UPDATE, DELETE) modify the transaction buffer and require `conn.commit()` to persist to the database file.",
            "Step 4: Confirm transaction completion and constraint behavior."
        ]
        concept = "Relational Data Modeling & SQLite Driver Operations: ACID transaction management and foreign key constraints in web applications."
        exam_trick = "Always call `conn.commit()` after INSERT or UPDATE; otherwise, changes disappear when the connection closes!"
        trap_alert = "Using Python string formatting (`f'SELECT... {user_input}'`) which leaves the database vulnerable to SQL injection."

    else:
        step_by_step = [
            "Step 1: Analyze the problem stem and identify the fundamental IITM MAD 1 syllabus topic being assessed.",
            "Step 2: Trace the logic, code execution, or parameter requirements step-by-step against standard web engineering conventions.",
            "Step 3: Systematically evaluate and eliminate incorrect answer choices based on syntax and protocol specifications.",
            "Step 4: Verify that the selected option aligns precisely with the verified course answer key."
        ]
        concept = f"Core Technical Mastery in {subtopic}: Accurate application of full-stack web principles and rigorous debugging."
        exam_trick = "Eliminate syntactically invalid or extreme answer options first to quickly zero in on the correct choice."
        trap_alert = "Watch out for subtle naming, case-sensitivity, and parameter order traps common in timed exams."

    return {
        "correct_label": correct_label,
        "correct_text": correct_text,
        "step_by_step": step_by_step,
        "concept": concept,
        "exam_trick": exam_trick,
        "trap_alert": trap_alert
    }

# Apply accurate classification and updated explanations
changed_topics = 0
for q in questions:
    old_week = q.get("week")
    old_subtopic = q.get("subtopic")
    new_week, new_subtopic = classify_question(q)
    
    if new_week != old_week or new_subtopic != old_subtopic:
        changed_topics += 1
        
    q["week"] = new_week
    q["subtopic"] = new_subtopic
    q["explanation"] = generate_explanation(q, new_week, new_subtopic)

print(f"Reclassified {changed_topics} questions to their accurate week and subtopic.")

# Save to data/questions.json
with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)
print(f"Updated {DATA_FILE}")

# Save to data/questions_data.js
with open(JS_DATA_FILE, "w", encoding="utf-8") as f:
    f.write("// IIT Madras Modern Application Development 1 (MAD 1 / AppDev1) Question Bank with Solutions\n")
    f.write("window.MAD1_QUESTIONS = ")
    json.dump(questions, f, indent=2, ensure_ascii=False)
    f.write(";\n")
print(f"Updated {JS_DATA_FILE}")

# Update stats.json with accurate counts
type_counts = Counter(q.get("question_type", "MCQ") for q in questions)
week_counts = Counter(q.get("week") for q in questions)
subtopic_counts = Counter(q.get("subtopic") for q in questions)

stats_payload = {
    "total_questions": len(questions),
    "type_counts": dict(type_counts),
    "week_counts": dict(week_counts),
    "subtopic_counts": dict(subtopic_counts)
}
with open(STATS_FILE, "w", encoding="utf-8") as f:
    json.dump(stats_payload, f, indent=2)
print(f"Updated {STATS_FILE}")

print("Distribution:")
for w, c in week_counts.items():
    print(f"  {w}: {c}")
