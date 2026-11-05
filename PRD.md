# Product Requirements Document (PRD) - MAD 1 PYQ & JEE CBT Test Platform

## Tasks Breakdown

- [ ] **Task 1: Establish Git & 4-Tier Configuration Baseline (`/addgit` + `/addconfig4`)**
  - Initialize local Git repository on `main` branch.
  - Generate comprehensive `.gitignore` tailored to Python, web assets, and raw binary archives.
  - Create baseline commit.
  - Create remote GitHub repository via GitHub CLI (`gh repo create mad1-pyq-jee-platform --public --source=. --remote=origin --push`) and configure upstream tracking.

- [ ] **Task 2: Multi-Paper MAD 1 Scanner & Visual Card Cropper**
  - Scan all candidate question paper PDFs in `C:\Users\avesh\Desktop\PYQS`, identifying all papers containing the official `Appdev1` / `AppDev1` / `AppDev-1` section.
  - Filter out zero-mark subject confirmation prompts.
  - Crop 150-DPI high-resolution visual question cards capturing complete problem stems, code blocks, tables, and option choices.
  - Extract verbatim question text, option choices, question type (MCQ, MSQ, SA), marks, and official answer keys.

- [ ] **Task 3: Exact Deduplication Engine & 4-Week Syllabus Classifier**
  - Implement normalized text and cross-slot deduplication to merge identical questions from parallel exam slots into single records with accumulated `source_papers` citations.
  - Integrate Windows Native OCR (`winrt`) to extract verbatim stems from embedded image snippets.
  - Classify unique questions into the official 4-week syllabus taxonomy with granular subcategories:
    - Week 1: Internet Architecture, HTTP & Network Calculations
    - Week 2: HTML5, CSS3, Box Model & Form Controls
    - Week 3: Backend Python, Flask Essentials, Routing & Request Handling
    - Week 4: Jinja2 Templating, Dynamic Rendering, SQLite & CRUD Applications
  - Generate structured `data/questions.json`, `data/stats.json`, and standalone bundle `data/questions_data.js`.

- [ ] **Task 4: Publication-Quality Categorized PDF Generator (`generate_pdf.py`)**
  - Build `scripts/generate_pdf.py` using ReportLab to render `mad1_questions_categorized.pdf`.
  - Format categorized questions by Week and Subtopic with running headers, footers, page numbering, embedded question cards, and verified answer keys.

- [ ] **Task 5: Interactive JEE CBT Examination Web Application & Admin Control Panel**
  - Develop `index.html`, `css/jee_style.css`, and `js/jee_app.js` replicating the NTA/JEE CBT examination system.
  - Embed full authentication system (`js/auth.js`) supporting Email & Roll Number login, demo sign-ins, and persistent local storage.
  - Build Admin Control Panel (`js/admin.js`) with system metrics, user controls, exam log viewer, question bank explorer, and data export.
  - Provide interactive Exam Mode (countdown timer, palette sidebar, mark for review, clear response), "🎲 Random Question" / "Quick Random Practice" modes, and comprehensive scorecard review.

- [ ] **Task 6: Automated Test Verification, CodeRabbit QA & Git Auto-Push**
  - Write test suite `tests/test_platform.py` verifying question schema, PDF integrity, image resolution, web linking, and authentication RBAC.
  - Run CodeRabbit code review audit (`coderabbit review --agent`) and fix any flagged issues.
  - Commit atomic changes and auto-push upstream to GitHub remote.
