# Goal Specification: IIT Madras MAD 1 (Modern Application Development 1) PYQ & CBT Platform

## 1. Objective
Extract every question verbatim from all past year question papers for **Modern Application Development 1 (MAD 1 / AppDev1)** in `C:\Users\avesh\Desktop\PYQS`, deduplicate questions identically across parallel batches, categorize them into the official 4-week syllabus taxonomy with granular subtopics, crop 150-DPI visual cards for every question, compile a publication-grade PDF (`mad1_questions_categorized.pdf`), build an interactive JEE CBT examination web application with complete authentication, session management, and admin dashboard, configure automated verification tests, and deploy publicly to GitHub Pages.

## 2. Acceptance Criteria
- [ ] Precision multi-paper scanner discovers all exam papers containing `Appdev1` / `AppDev1` / `AppDev-1` sections across `C:\Users\avesh\Desktop\PYQS`.
- [ ] Filter out 0-mark confirmation and hall ticket prompts.
- [ ] Crop 150-DPI visual question cards for every question capturing complete problem stem, terminal commands, HTML/CSS/Flask code blocks, and option choices.
- [ ] Extract question text verbatim with options, question types (MCQ, MSQ, SA), marks, and official keys.
- [ ] Windows Native OCR (`winrt`) transcription of code and text from cropped question cards.
- [ ] Clean deduplication of parallel slots into single records with accumulated source paper citations.
- [ ] Categorize into official 4-week MAD 1 syllabus taxonomy:
  - Week 1: Internet Architecture, HTTP & Network Calculations
  - Week 2: HTML5, CSS3, Box Model & Form Controls
  - Week 3: Backend Python, Flask Essentials, Routing & Request Handling
  - Week 4: Jinja2 Templating, Dynamic Rendering, SQLite & CRUD Applications
- [ ] Compile publication PDF (`mad1_questions_categorized.pdf`) with ReportLab, running headers, footers, visual cards, verified answer keys, and table of contents.
- [ ] Build JEE CBT Examination web platform (`index.html`, `css/jee_style.css`, `js/auth.js`, `js/admin.js`, `js/jee_app.js`):
  - Student & Admin authentication supporting Email & Roll Number login.
  - Quick demo sign-in buttons for Student and Faculty Admin.
  - Admin control panel with KPI cards, question bank explorer, candidate user manager, attempts feed, and CSV/JSON export.
  - Full JEE CBT test engine with 180 min timer, color-coded palette, review flags, and post-exam scorecard.
  - "🎲 Random Question" / "Quick Random Practice" modes across header, metadata bar, palette, and footer.
- [ ] Comprehensive automated test suite (`tests/test_platform.py`) verifying schema, card files, PDF size, web linking, answers, and authentication RBAC.
- [ ] Complete remote repository setup (`gh repo create mad1-pyq-jee-platform --public`), upstream tracking on `main`, and live GitHub Pages deployment.

## 3. Constraints
- Strict Tech Stack Compliance: Vanilla JS, CSS3, HTML5, Python 3.13, PyMuPDF, ReportLab.
- Zero mockups or placeholder buttons.
- Verbatim question extraction without omissions.
