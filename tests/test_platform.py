"""
Comprehensive Test Suite for IIT Madras Modern Application Development 1 (MAD 1) CBT Examination Platform
"""
import os
import json
import unittest
import subprocess
import fitz  # PyMuPDF

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TestMAD1Platform(unittest.TestCase):
    def setUp(self):
        self.data_path = os.path.join(PROJECT_ROOT, "data", "questions.json")
        self.pdf_path = os.path.join(PROJECT_ROOT, "mad1_questions_categorized.pdf")
        self.index_html_path = os.path.join(PROJECT_ROOT, "index.html")

    def test_01_questions_json_exists_and_valid(self):
        self.assertTrue(os.path.exists(self.data_path), "data/questions.json must exist")
        with open(self.data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 301, f"Expected 301 unique questions, got {len(data)}")

    def test_02_questions_schema_integrity(self):
        with open(self.data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        required_keys = {"id", "raw_q_id", "week", "subtopic", "question_type", "marks", "card_image", "correct_answer"}
        subtopics = set()
        for i, q in enumerate(data):
            for k in required_keys:
                self.assertIn(k, q, f"Question at index {i} missing key: {k}")
            self.assertIn(q["question_type"], ["MCQ", "MSQ", "SA"], f"Invalid type in {q['id']}")
            self.assertGreater(q["marks"], 0, f"Marks must be > 0 in {q['id']}")
            if q["question_type"] in ["MCQ", "MSQ"]:
                self.assertGreaterEqual(len(q.get("options", [])), 2, f"MCQ/MSQ missing options in {q['id']}")
            subtopics.add(q["subtopic"])
        self.assertGreaterEqual(len(subtopics), 15, f"Expected >= 15 subtopics, got {len(subtopics)}")

    def test_03_week_distribution(self):
        with open(self.data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        week_counts = {}
        for q in data:
            prefix = q["week"].split(":")[0].strip()
            week_counts[prefix] = week_counts.get(prefix, 0) + 1

        self.assertEqual(week_counts.get("Week 1"), 50, f"Week 1 must contain 50 questions (got {week_counts.get('Week 1')})")
        self.assertEqual(week_counts.get("Week 2"), 115, f"Week 2 must contain 115 questions (got {week_counts.get('Week 2')})")
        self.assertEqual(week_counts.get("Week 3"), 78, f"Week 3 must contain 78 questions (got {week_counts.get('Week 3')})")
        self.assertEqual(week_counts.get("Week 4"), 58, f"Week 4 must contain 58 questions (got {week_counts.get('Week 4')})")
        self.assertEqual(sum(week_counts.values()), 301, "Total questions across all weeks must equal 301")

    def test_04_card_images_exist_and_non_empty(self):
        with open(self.data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for q in data:
            card_rel = q.get("card_image")
            self.assertTrue(card_rel, f"Missing card_image for {q['id']}")
            full_card_path = os.path.join(PROJECT_ROOT, card_rel.replace("/", os.sep))
            self.assertTrue(os.path.exists(full_card_path), f"Card file does not exist: {full_card_path}")
            size = os.path.getsize(full_card_path)
            self.assertGreater(size, 1024, f"Card file is suspiciously small ({size} bytes): {full_card_path}")

    def test_05_pdf_publication_integrity(self):
        self.assertTrue(os.path.exists(self.pdf_path), "mad1_questions_categorized.pdf must exist")
        pdf_size = os.path.getsize(self.pdf_path)
        self.assertGreater(pdf_size, 15 * 1024 * 1024, f"PDF must be > 15MB (got {pdf_size / (1024*1024):.2f} MB)")
        self.assertLess(pdf_size, 90 * 1024 * 1024, f"PDF must be < 90MB for GitHub limits (got {pdf_size / (1024*1024):.2f} MB)")
        
        doc = fitz.open(self.pdf_path)
        self.assertGreater(len(doc), 200, f"Expected > 200 pages in categorized PDF, got {len(doc)}")
        page1_text = doc[0].get_text().lower()
        self.assertTrue("modern application development 1" in page1_text or "mad 1" in page1_text, "Title page must mention MAD 1")
        self.assertIn("301", page1_text)
        doc.close()

    def test_06_web_assets_and_html_linking(self):
        assets = [
            os.path.join(PROJECT_ROOT, "css", "jee_style.css"),
            os.path.join(PROJECT_ROOT, "js", "auth.js"),
            os.path.join(PROJECT_ROOT, "js", "admin.js"),
            os.path.join(PROJECT_ROOT, "js", "jee_app.js"),
            os.path.join(PROJECT_ROOT, "data", "questions_data.js")
        ]
        for a in assets:
            self.assertTrue(os.path.exists(a), f"Asset missing: {a}")
            self.assertGreater(os.path.getsize(a), 100, f"Asset empty or too small: {a}")

        with open(self.index_html_path, "r", encoding="utf-8") as f:
            html = f.read()

        self.assertIn("MODERN APPLICATION DEVELOPMENT 1", html)
        self.assertIn("data/questions_data.js", html)
        self.assertIn("js/auth.js", html)
        self.assertIn("js/admin.js", html)
        self.assertIn("js/jee_app.js", html)
        self.assertIn("css/jee_style.css", html)
        self.assertIn("btnQuickRandom", html)
        self.assertIn("btnFooterRandom", html)

    def test_07_auth_system_and_roles(self):
        auth_js_path = os.path.join(PROJECT_ROOT, "js", "auth.js")
        jee_app_path = os.path.join(PROJECT_ROOT, "js", "jee_app.js")
        with open(auth_js_path, "r", encoding="utf-8") as f:
            auth_src = f.read()
        with open(jee_app_path, "r", encoding="utf-8") as f:
            jee_src = f.read()

        # Check export bindings
        self.assertIn("root.MAD1Auth = authInstance;", auth_src)
        self.assertIn("root.Auth = authInstance;", auth_src)
        self.assertIn("getAuth()", jee_src)
        self.assertIn("getAdmin()", jee_src)

        # Run Node.js test harness against auth.js
        node_script = """
        const storage = {};
        global.localStorage = {
            getItem: (k) => storage[k] || null,
            setItem: (k, v) => { storage[k] = String(v); },
            removeItem: (k) => { delete storage[k]; }
        };
        global.sessionStorage = Object.assign({}, global.localStorage);
        const Auth = require('./js/auth.js');

        // Test 1: Email login
        const r1 = Auth.login('student@iitm.ac.in', 'Student@123', true);
        if (!r1.success || r1.user.rollNo !== '24DS109284') process.exit(1);

        // Test 2: Roll number login
        const r2 = Auth.login('24DS109284', 'Student@123', true);
        if (!r2.success || r2.user.email !== 'student@iitm.ac.in') process.exit(2);

        // Test 3: Admin roll number login case-insensitively
        const r3 = Auth.login('admin-001', 'Admin@123', true);
        if (!r3.success || r3.user.role !== 'admin') process.exit(3);

        // Test 4: Wrong credentials
        const r4 = Auth.login('student@iitm.ac.in', 'WrongPass!', true);
        if (r4.success) process.exit(4);

        // Test 5: Signup
        const s1 = Auth.signUp('Automation User', 'auto@iitm.ac.in', '24DS888777', 'Pass@123', 'student');
        if (!s1.success || s1.user.rollNo !== '24DS888777') process.exit(5);

        // Test 6: Duplicate prevention
        const s2 = Auth.signUp('Automation User', 'auto@iitm.ac.in', '24DS888777', 'Pass@123', 'student');
        if (s2.success) process.exit(6);

        // Test 7: Logout
        Auth.logout();
        if (Auth.getCurrentUser() !== null) process.exit(7);

        console.log('ALL_AUTH_CHECKS_PASSED');
        """
        res = subprocess.run(
            ["node", "-e", node_script],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        self.assertEqual(res.returncode, 0, f"Auth test harness failed: {res.stderr}\n{res.stdout}")
        self.assertIn("ALL_AUTH_CHECKS_PASSED", res.stdout)

    def test_08_explanations_and_solution_drawer_integrity(self):
        with open(self.data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        self.assertEqual(len(data), 301)
        for q in data:
            self.assertIn("explanation", q, f"Missing explanation in {q['id']}")
            exp = q["explanation"]
            self.assertIn("correct_label", exp, f"Missing correct_label in {q['id']}")
            self.assertIn("step_by_step", exp, f"Missing step_by_step in {q['id']}")
            self.assertIsInstance(exp["step_by_step"], list, f"step_by_step must be list in {q['id']}")
            self.assertGreaterEqual(len(exp["step_by_step"]), 3, f"Expected >= 3 explanation steps in {q['id']}")
            self.assertIn("concept", exp, f"Missing concept in {q['id']}")
            self.assertIn("exam_trick", exp, f"Missing exam_trick in {q['id']}")
            self.assertIn("trap_alert", exp, f"Missing trap_alert in {q['id']}")
            self.assertTrue(len(exp["concept"]) > 10, f"Concept text too short in {q['id']}")
            self.assertTrue(len(exp["exam_trick"]) > 10, f"Exam trick too short in {q['id']}")
            self.assertTrue(len(exp["trap_alert"]) > 10, f"Trap alert too short in {q['id']}")

        with open(self.index_html_path, "r", encoding="utf-8") as f:
            html = f.read()

        self.assertIn("btnToggleSolution", html, "index.html must have btnToggleSolution")
        self.assertIn("solutionDrawer", html, "index.html must have solutionDrawer")
        self.assertIn("solCorrectLabel", html, "index.html must have solCorrectLabel")
        self.assertIn("solStepsList", html, "index.html must have solStepsList")
        self.assertIn("solConceptText", html, "index.html must have solConceptText")
        self.assertIn("solTrickText", html, "index.html must have solTrickText")
        self.assertIn("solTrapText", html, "index.html must have solTrapText")

        jee_app_path = os.path.join(PROJECT_ROOT, "js", "jee_app.js")
        with open(jee_app_path, "r", encoding="utf-8") as f:
            jee_src = f.read()

        self.assertIn("toggleSolutionDrawer", jee_src, "jee_app.js must define toggleSolutionDrawer")
        self.assertIn("renderCurrentSolution", jee_src, "jee_app.js must define renderCurrentSolution")
        self.assertIn("btnToggleSolution", jee_src, "jee_app.js must reference btnToggleSolution")

if __name__ == "__main__":
    unittest.main()
