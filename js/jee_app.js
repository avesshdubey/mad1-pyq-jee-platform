// JEE Examination CBT Engine - Modern Application Development 1 (MAD 1 / AppDev1)
(function () {
    'use strict';

    function getAuth() {
        return window.MAD1Auth || window.Auth || window.SCAuth || window.MLTAuth || window.MLFAuth;
    }

    function getAdmin() {
        return window.MAD1Admin || window.Admin || window.SCAdmin || window.MLTAdmin || window.MLFAdmin;
    }

    // State Variables
    let allQuestions = [];
    let currentQuestions = [];
    let currentIndex = 0;
    let currentWeekFilter = 'ALL';
    let currentSubtopicFilter = 'ALL';
    
    // User responses: questionId -> { status, selectedOptions, value }
    let responses = {};

    // Timer state
    let totalSeconds = 180 * 60; // 180 minutes
    let timerInterval = null;
    let isPaused = false;
    let isExamSubmitted = false;
    let currentZoom = 1.0;

    // DOM Elements
    const elements = {
        timerDisplay: document.getElementById('timerDisplay'),
        pauseTimerBtn: document.getElementById('pauseTimerBtn'),
        sectionTabs: document.getElementById('sectionTabs'),
        subtopicSelect: document.getElementById('subtopicFilterSelect'),
        paletteSecLabel: document.getElementById('paletteSecLabel'),
        paletteGrid: document.getElementById('paletteGrid'),
        
        // Header & User elements
        headerUserName: document.getElementById('headerUserName'),
        headerUserRoll: document.getElementById('headerUserRoll'),
        headerUserRole: document.getElementById('headerUserRole'),
        btnToggleAdminView: document.getElementById('btnToggleAdminView'),
        btnToggleExamView: document.getElementById('btnToggleExamView'),
        btnLogout: document.getElementById('btnLogout'),
        
        // Views
        examInterfaceView: document.getElementById('examInterfaceView'),
        adminDashboardView: document.getElementById('adminDashboardView'),
        scorecardView: document.getElementById('scorecardView'),
        examMain: document.getElementById('examMain'),
        
        // Question Display
        qNumberLabel: document.getElementById('qNumberLabel'),
        qTypeBadge: document.getElementById('qTypeBadge'),
        qMarksPositive: document.getElementById('qMarksPositive'),
        qMarksNegative: document.getElementById('qMarksNegative'),
        qCardImage: document.getElementById('qCardImage'),
        qStemText: document.getElementById('qStemText'),
        qOptionsContainer: document.getElementById('qOptionsContainer'),
        
        // Zoom & Preview Modal Elements
        btnZoomIn: document.getElementById('btnZoomIn'),
        btnZoomOut: document.getElementById('btnZoomOut'),
        btnZoomReset: document.getElementById('btnZoomReset'),
        zoomLevelText: document.getElementById('zoomLevelText'),
        btnZoomModal: document.getElementById('btnZoomModal'),
        examImageModal: document.getElementById('examImageModal'),
        btnExamImageModalClose: document.getElementById('btnExamImageModalClose'),
        examImageModalImg: document.getElementById('examImageModalImg'),
        examImageModalTitle: document.getElementById('examImageModalTitle'),

        // Action Buttons
        btnMarkReview: document.getElementById('btnMarkReview'),
        btnClearResponse: document.getElementById('btnClearResponse'),
        btnPrev: document.getElementById('btnPrev'),
        btnNext: document.getElementById('btnNext'),
        btnSaveNext: document.getElementById('btnSaveNext'),
        btnSubmitExam: document.getElementById('btnSubmitExam'),
        btnQuickRandom: document.getElementById('btnQuickRandom'),
        btnMetaRandom: document.getElementById('btnMetaRandom'),
        btnFooterRandom: document.getElementById('btnFooterRandom'),
        
        // Legend Counters
        countAnswered: document.getElementById('countAnswered'),
        countNotAnswered: document.getElementById('countNotAnswered'),
        countNotVisited: document.getElementById('countNotVisited'),
        countMarkedReview: document.getElementById('countMarkedReview'),
        countAnsMarkedReview: document.getElementById('countAnsMarkedReview'),
        
        // Scorecard Elements
        resTotalScore: document.getElementById('resTotalScore'),
        resMaxMarks: document.getElementById('resMaxMarks'),
        resAccuracy: document.getElementById('resAccuracy'),
        resAttempted: document.getElementById('resAttempted'),
        resCorrect: document.getElementById('resCorrect'),
        resIncorrect: document.getElementById('resIncorrect'),
        scorecardTableBody: document.getElementById('scorecardTableBody'),
        btnReviewSolutions: document.getElementById('btnReviewSolutions'),
        btnRetakeExam: document.getElementById('btnRetakeExam'),
        btnScorecardAdminDashboard: document.getElementById('btnScorecardAdminDashboard'),
        
        // Auth Modal Elements
        authModal: document.getElementById('authModal'),
        tabLoginBtn: document.getElementById('tabLoginBtn'),
        tabSignupBtn: document.getElementById('tabSignupBtn'),
        formLogin: document.getElementById('formLogin'),
        formSignup: document.getElementById('formSignup'),
        authAlert: document.getElementById('authAlert'),
        btnQuickStudent: document.getElementById('btnQuickStudent'),
        btnQuickAdmin: document.getElementById('btnQuickAdmin')
    };

    // Initialize Application
    function init() {
        if (window.MAD1_QUESTIONS && Array.isArray(window.MAD1_QUESTIONS)) {
            loadQuestions(window.MAD1_QUESTIONS);
        } else {
            fetch('data/questions.json')
                .then(r => r.json())
                .then(data => loadQuestions(data))
                .catch(err => {
                    console.error("Failed to load questions:", err);
                    alert("Unable to load examination question bank. Please verify network or data files.");
                });
        }
    }

    function loadQuestions(data) {
        allQuestions = data;
        currentQuestions = [...allQuestions];

        // Initialize state for each question
        allQuestions.forEach(q => {
            responses[q.id] = {
                status: 'NOT_VISITED', // NOT_VISITED, NOT_ANSWERED, ANSWERED, MARKED_REVIEW, ANS_MARKED_REVIEW
                selectedOptions: [],
                value: ''
            };
        });

        // Dynamically compute and display week counts and total questions
        const weekCounts = {
            'ALL': allQuestions.length,
            'Week 1': 0,
            'Week 2': 0,
            'Week 3': 0,
            'Week 4': 0
        };
        allQuestions.forEach(q => {
            if (q.week.startsWith('Week 1')) weekCounts['Week 1']++;
            else if (q.week.startsWith('Week 2')) weekCounts['Week 2']++;
            else if (q.week.startsWith('Week 3')) weekCounts['Week 3']++;
            else if (q.week.startsWith('Week 4')) weekCounts['Week 4']++;
        });
        elements.sectionTabs.querySelectorAll('.sec-tab').forEach(tab => {
            const wk = tab.dataset.week;
            if (wk === 'ALL') tab.textContent = `All Weeks (${weekCounts['ALL']})`;
            else if (wk === 'Week 1') tab.textContent = `Week 1: Internet & HTTP (${weekCounts['Week 1']})`;
            else if (wk === 'Week 2') tab.textContent = `Week 2: HTML5 & CSS3 (${weekCounts['Week 2']})`;
            else if (wk === 'Week 3') tab.textContent = `Week 3: Flask & Routing (${weekCounts['Week 3']})`;
            else if (wk === 'Week 4') tab.textContent = `Week 4: Jinja2 & SQLite (${weekCounts['Week 4']})`;
        });
        elements.countNotVisited.textContent = allQuestions.length;

        buildSubtopicDropdown();
        applyFilter();
        bindEvents();

        // Check authentication & initialize UI/timer
        checkAuthAndSetupUI();
    }

    // ==================== AUTHENTICATION & ROLE GUARDS ====================
    function checkAuthAndSetupUI() {
        const Auth = getAuth();
        if (!Auth) return;

        const curUser = Auth.getCurrentUser();

        if (curUser) {
            // User is signed in
            elements.authModal.style.display = 'none';
            elements.headerUserName.textContent = curUser.name;
            elements.headerUserRoll.textContent = curUser.rollNo;
            elements.headerUserRole.textContent = curUser.role.toUpperCase();

            if (curUser.role === 'admin') {
                elements.btnToggleAdminView.style.display = 'inline-block';
                // Initialize Admin Controller
                const Admin = getAdmin();
                if (Admin) {
                    Admin.init(allQuestions);
                }
            } else {
                elements.btnToggleAdminView.style.display = 'none';
                elements.btnToggleExamView.style.display = 'none';
                if (!isExamSubmitted) {
                    elements.examInterfaceView.style.display = 'block';
                    elements.scorecardView.style.display = 'none';
                }
                elements.adminDashboardView.style.display = 'none';
            }

            // Start timer only if exam is in progress
            if (!isExamSubmitted && elements.examInterfaceView.style.display !== 'none') {
                startTimer();
            }
        } else {
            // User is NOT signed in: trigger auth modal and stop timer
            stopTimer();
            elements.authModal.style.display = 'flex';
            elements.btnToggleAdminView.style.display = 'none';
            elements.btnToggleExamView.style.display = 'none';
        }
    }

    function resetExamState() {
        isExamSubmitted = false;
        stopTimer();
        responses = {};
        allQuestions.forEach(q => {
            responses[q.id] = {
                status: 'NOT_VISITED',
                selectedOptions: [],
                value: ''
            };
        });
        currentIndex = 0;
        totalSeconds = 180 * 60;
        isPaused = false;
        updateTimerDisplay();
        elements.countNotVisited.textContent = allQuestions.length;
        applyFilter();
    }

    function showAuthAlert(msg, isSuccess = false) {
        elements.authAlert.textContent = msg;
        elements.authAlert.className = `auth-alert ${isSuccess ? 'success' : 'error'}`;
        elements.authAlert.style.display = 'block';
    }

    function hideAuthAlert() {
        elements.authAlert.style.display = 'none';
    }

    function setZoom(val) {
        currentZoom = Math.min(2.5, Math.max(0.7, Math.round(val * 100) / 100));
        if (elements.qCardImage) {
            elements.qCardImage.style.width = `${currentZoom * 100}%`;
            elements.qCardImage.style.maxWidth = currentZoom > 1 ? 'none' : '100%';
        }
        if (elements.zoomLevelText) {
            elements.zoomLevelText.textContent = `${Math.round(currentZoom * 100)}%`;
        }
    }

    function buildSubtopicDropdown() {
        const subtopicCounts = {};
        allQuestions.forEach(q => {
            const matchWeek = (currentWeekFilter === 'ALL' || q.week.startsWith(currentWeekFilter));
            if (matchWeek && q.subtopic) {
                subtopicCounts[q.subtopic] = (subtopicCounts[q.subtopic] || 0) + 1;
            }
        });

        const totalInWeek = Object.values(subtopicCounts).reduce((a, b) => a + b, 0);
        elements.subtopicSelect.innerHTML = `<option value="ALL">All Subtopics (${totalInWeek})</option>`;
        Object.keys(subtopicCounts).sort().forEach(st => {
            const opt = document.createElement('option');
            opt.value = st;
            opt.textContent = `${st} (${subtopicCounts[st]})`;
            elements.subtopicSelect.appendChild(opt);
        });
        elements.subtopicSelect.value = currentSubtopicFilter;
    }

    function applyFilter() {
        currentQuestions = allQuestions.filter(q => {
            const matchWeek = (currentWeekFilter === 'ALL' || q.week.startsWith(currentWeekFilter));
            const matchSub = (currentSubtopicFilter === 'ALL' || q.subtopic === currentSubtopicFilter);
            return matchWeek && matchSub;
        });

        if (currentQuestions.length === 0) {
            currentQuestions = allQuestions;
            currentWeekFilter = 'ALL';
            currentSubtopicFilter = 'ALL';
            elements.subtopicSelect.value = 'ALL';
        }

        currentIndex = 0;
        updatePaletteSecLabel();
        renderPalette();
        renderCurrentQuestion();
        updateLegendCounters();
    }

    function updatePaletteSecLabel() {
        let label = 'All MAD 1 Questions';
        if (currentWeekFilter === 'Week 1') label = 'Week 1: Internet & HTTP';
        else if (currentWeekFilter === 'Week 2') label = 'Week 2: HTML5 & CSS3';
        else if (currentWeekFilter === 'Week 3') label = 'Week 3: Flask & Routing';
        else if (currentWeekFilter === 'Week 4') label = 'Week 4: Jinja2 & SQLite';
        
        if (currentSubtopicFilter !== 'ALL') {
            label += ` (${currentSubtopicFilter})`;
        }
        elements.paletteSecLabel.textContent = `${label} [${currentQuestions.length}]`;
    }

    function startTimer() {
        if (timerInterval) clearInterval(timerInterval);
        timerInterval = setInterval(() => {
            const Auth = getAuth();
            const curUser = Auth ? Auth.getCurrentUser() : null;
            const isExamActive = curUser && elements.examInterfaceView && elements.examInterfaceView.style.display !== 'none' && !isExamSubmitted;
            
            if (!isExamActive) {
                return;
            }

            if (!isPaused && totalSeconds > 0) {
                totalSeconds--;
                updateTimerDisplay();
            } else if (totalSeconds <= 0) {
                clearInterval(timerInterval);
                timerInterval = null;
                alert("Time's up! Submitting examination automatically.");
                submitExam();
            }
        }, 1000);
    }

    function stopTimer() {
        if (timerInterval) {
            clearInterval(timerInterval);
            timerInterval = null;
        }
    }

    function updateTimerDisplay() {
        const hrs = Math.floor(totalSeconds / 3600);
        const mins = Math.floor((totalSeconds % 3600) / 60);
        const secs = totalSeconds % 60;
        elements.timerDisplay.textContent = 
            `${String(hrs).padStart(2, '0')}:${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
        
        if (totalSeconds < 300) {
            elements.timerDisplay.classList.add('urgent');
        } else {
            elements.timerDisplay.classList.remove('urgent');
        }
    }

    function renderCurrentQuestion() {
        if (!currentQuestions || currentQuestions.length === 0) return;
        const q = currentQuestions[currentIndex];
        const resp = responses[q.id];

        // If NOT_VISITED, transition to NOT_ANSWERED
        if (resp.status === 'NOT_VISITED') {
            resp.status = 'NOT_ANSWERED';
            updateLegendCounters();
            updatePaletteButton(currentIndex);
        }

        // Header info
        elements.qNumberLabel.textContent = `Question ${currentIndex + 1} of ${currentQuestions.length} (${q.id})`;
        elements.qTypeBadge.textContent = q.question_type;
        elements.qMarksPositive.textContent = `+${q.marks}`;
        elements.qMarksNegative.textContent = `-0`;

        // Card image display & Zoom reset
        setZoom(1.0);
        if (q.card_image) {
            elements.qCardImage.src = q.card_image;
            elements.qCardImage.style.display = 'block';
            elements.qStemText.style.display = 'none'; // Question Card Image is authoritative
            elements.qCardImage.onerror = () => {
                elements.qCardImage.style.display = 'none';
                elements.qStemText.style.display = 'block';
                elements.qStemText.textContent = q.question_text || 'Visual card image unavailable.';
            };
        } else {
            elements.qCardImage.style.display = 'none';
            if (q.question_text && q.question_text.trim()) {
                elements.qStemText.textContent = q.question_text;
                elements.qStemText.style.display = 'block';
            } else {
                elements.qStemText.style.display = 'none';
            }
        }

        // Render Option Inputs
        renderOptions(q, resp);
        updateNavButtons();
    }

    function renderOptions(q, resp) {
        elements.qOptionsContainer.innerHTML = '';

        if (q.question_type === 'MCQ') {
            const list = document.createElement('div');
            list.className = 'options-list';
            q.options.forEach((opt, idx) => {
                const label = document.createElement('label');
                label.className = 'option-item';
                
                const isSelected = resp.selectedOptions.includes(opt.option_id);
                if (isSelected) {
                    label.classList.add('selected');
                }
                
                const radio = document.createElement('input');
                radio.type = 'radio';
                radio.name = `opt_${q.id}`;
                radio.value = opt.option_id;
                radio.checked = isSelected;
                
                radio.addEventListener('change', () => {
                    resp.selectedOptions = [opt.option_id];
                    list.querySelectorAll('.option-item').forEach(l => l.classList.remove('selected'));
                    label.classList.add('selected');
                });

                const letterBadge = document.createElement('span');
                letterBadge.className = 'option-letter';
                letterBadge.textContent = String.fromCharCode(65 + idx);

                const txt = document.createElement('span');
                txt.className = 'option-text';
                let optText = (opt.text || '').trim();
                if (!optText || optText === `Option ${String.fromCharCode(65 + idx)}` || optText.startsWith('640653')
                    || /^---PAGE_\d+---$/.test(optText) || ['Java', 'MLF', 'MLT', 'SC', 'Appdev1', 'AppDev1'].includes(optText)) {
                    optText = `Option ${String.fromCharCode(65 + idx)}`;
                }
                txt.textContent = optText;

                label.appendChild(radio);
                label.appendChild(letterBadge);
                label.appendChild(txt);
                list.appendChild(label);
            });
            elements.qOptionsContainer.appendChild(list);

        } else if (q.question_type === 'MSQ') {
            const list = document.createElement('div');
            list.className = 'options-list';
            const note = document.createElement('div');
            note.className = 'msq-note';
            note.style.cssText = 'font-size: 12px; font-weight: 600; color: #d97706; background: #fffbeb; border: 1px solid #fde68a; padding: 6px 12px; border-radius: 4px; margin-bottom: 8px;';
            note.textContent = 'ℹ️ Multiple Select Question: One or more options may be correct. Select all that apply.';
            list.appendChild(note);

            q.options.forEach((opt, idx) => {
                const label = document.createElement('label');
                label.className = 'option-item';
                
                const isSelected = resp.selectedOptions.includes(opt.option_id);
                if (isSelected) {
                    label.classList.add('selected');
                }
                
                const check = document.createElement('input');
                check.type = 'checkbox';
                check.name = `opt_${q.id}`;
                check.value = opt.option_id;
                check.checked = isSelected;
                
                check.addEventListener('change', () => {
                    if (check.checked) {
                        if (!resp.selectedOptions.includes(opt.option_id)) {
                            resp.selectedOptions.push(opt.option_id);
                        }
                        label.classList.add('selected');
                    } else {
                        resp.selectedOptions = resp.selectedOptions.filter(id => id !== opt.option_id);
                        label.classList.remove('selected');
                    }
                });

                const letterBadge = document.createElement('span');
                letterBadge.className = 'option-letter';
                letterBadge.textContent = String.fromCharCode(65 + idx);

                const txt = document.createElement('span');
                txt.className = 'option-text';
                let optText = (opt.text || '').trim();
                if (!optText || optText === `Option ${String.fromCharCode(65 + idx)}` || optText.startsWith('640653')
                    || /^---PAGE_\d+---$/.test(optText) || ['Java', 'MLF', 'MLT', 'SC', 'Appdev1', 'AppDev1'].includes(optText)) {
                    optText = `Option ${String.fromCharCode(65 + idx)}`;
                }
                txt.textContent = optText;

                label.appendChild(check);
                label.appendChild(letterBadge);
                label.appendChild(txt);
                list.appendChild(label);
            });
            elements.qOptionsContainer.appendChild(list);

        } else if (q.question_type === 'SA') {
            const saBox = document.createElement('div');
            saBox.className = 'sa-input-container';
            const label = document.createElement('label');
            label.textContent = 'Enter Numerical Answer / Output:';
            const input = document.createElement('input');
            input.type = 'text';
            input.className = 'form-control sa-input';
            input.placeholder = 'e.g. 250 or 72';
            input.value = resp.value || '';
            input.addEventListener('input', (e) => {
                resp.value = e.target.value.trim();
            });

            saBox.appendChild(label);
            saBox.appendChild(input);
            elements.qOptionsContainer.appendChild(saBox);
        }
    }

    function renderPalette() {
        elements.paletteGrid.innerHTML = '';
        currentQuestions.forEach((q, idx) => {
            const btn = document.createElement('button');
            btn.className = 'pal-btn';
            btn.textContent = idx + 1;
            btn.dataset.index = idx;
            btn.addEventListener('click', () => {
                navigateToQuestion(idx);
            });
            updatePaletteBtnClass(btn, responses[q.id].status, idx === currentIndex);
            elements.paletteGrid.appendChild(btn);
        });
    }

    function updatePaletteButton(idx) {
        const btns = elements.paletteGrid.children;
        if (btns[idx]) {
            const q = currentQuestions[idx];
            updatePaletteBtnClass(btns[idx], responses[q.id].status, idx === currentIndex);
        }
    }

    function updatePaletteBtnClass(btn, status, isCurrent) {
        btn.className = 'pal-btn';
        if (status === 'ANSWERED') btn.classList.add('status-answered');
        else if (status === 'NOT_ANSWERED') btn.classList.add('status-not-answered');
        else if (status === 'NOT_VISITED') btn.classList.add('status-not-visited');
        else if (status === 'MARKED_REVIEW') btn.classList.add('status-marked-review');
        else if (status === 'ANS_MARKED_REVIEW') btn.classList.add('status-ans-marked-review');

        if (isCurrent) {
            btn.classList.add('current-active');
        }
    }

    function updateNavButtons() {
        elements.btnPrev.disabled = (currentIndex === 0);
        elements.btnNext.disabled = (currentIndex === currentQuestions.length - 1);
    }

    function navigateToQuestion(newIndex) {
        if (newIndex >= 0 && newIndex < currentQuestions.length) {
            const prevIdx = currentIndex;
            currentIndex = newIndex;
            updatePaletteButton(prevIdx);
            renderCurrentQuestion();
            updatePaletteButton(currentIndex);
        }
    }

    // "🎲 Random Question" / "Quick Random Practice" selector
    function selectRandomQuestion() {
        if (!currentQuestions || currentQuestions.length === 0) return;
        if (currentQuestions.length === 1) {
            navigateToQuestion(0);
            return;
        }
        let randIdx = currentIndex;
        while (randIdx === currentIndex) {
            randIdx = Math.floor(Math.random() * currentQuestions.length);
        }
        navigateToQuestion(randIdx);
    }

    function updateLegendCounters() {
        let ans = 0, notAns = 0, notVis = 0, marked = 0, ansMarked = 0;
        const targetQuestions = (currentQuestions && currentQuestions.length > 0) ? currentQuestions : allQuestions;
        targetQuestions.forEach(q => {
            const st = responses[q.id].status;
            if (st === 'ANSWERED') ans++;
            else if (st === 'NOT_ANSWERED') notAns++;
            else if (st === 'NOT_VISITED') notVis++;
            else if (st === 'MARKED_REVIEW') marked++;
            else if (st === 'ANS_MARKED_REVIEW') ansMarked++;
        });

        elements.countAnswered.textContent = ans;
        elements.countNotAnswered.textContent = notAns;
        elements.countNotVisited.textContent = notVis;
        elements.countMarkedReview.textContent = marked;
        elements.countAnsMarkedReview.textContent = ansMarked;
    }

    // ==================== SUBMISSION & EVALUATION ====================
    function submitExam() {
        if (!confirm("Are you sure you want to finish and submit your examination? Once submitted, your scores and official solutions will be unlocked.")) {
            return;
        }

        let totalScore = 0;
        let maxMarks = 0;
        let correctCount = 0;
        let attemptedCount = 0;

        const categoryStats = {};

        allQuestions.forEach(q => {
            maxMarks += q.marks;
            const resp = responses[q.id];
            const w = q.week.split(':')[0].trim();
            const st = q.subtopic;

            if (!categoryStats[w]) categoryStats[w] = {};
            if (!categoryStats[w][st]) categoryStats[w][st] = { total: 0, correct: 0, incorrect: 0 };
            categoryStats[w][st].total++;

            let isAttempted = false;
            let isCorrect = false;
            let earned = 0;

            if (q.question_type === 'SA') {
                isAttempted = (resp.value && resp.value.trim() !== '');
            } else {
                isAttempted = (resp.selectedOptions && resp.selectedOptions.length > 0);
            }

            if (isAttempted) {
                attemptedCount++;
                const key = q.correct_answer || [];

                if (q.question_type === 'MCQ') {
                    isCorrect = key.length > 0 && key.includes(resp.selectedOptions[0]);
                } else if (q.question_type === 'MSQ') {
                    const sel = new Set(resp.selectedOptions);
                    isCorrect = key.length > 0 && sel.size === key.length && key.every(k => sel.has(k));
                } else if (q.question_type === 'SA') {
                    const v = parseFloat(resp.value);
                    isCorrect = !Number.isNaN(v) && key.some(ans => {
                        const m = ans.match(/^\s*(-?[\d.]+)\s*to\s*(-?[\d.]+)/);
                        if (m) return v >= parseFloat(m[1]) && v <= parseFloat(m[2]);
                        const exact = parseFloat(ans);
                        return !Number.isNaN(exact) && Math.abs(v - exact) < 1e-6;
                    });
                }

                if (isCorrect) {
                    correctCount++;
                    earned = q.marks;
                    totalScore += earned;
                    categoryStats[w][st].correct++;
                } else {
                    earned = 0; // Section Negative Marks : 0 in IITM MAD 1
                    categoryStats[w][st].incorrect++;
                }
            }

            resp.evaluation = {
                isAttempted,
                isCorrect,
                marksAwarded: earned
            };
        });

        // Set exam submitted and stop timer
        isExamSubmitted = true;
        stopTimer();

        // Calculate active section vs full syllabus stats
        const isSectionTest = currentWeekFilter !== 'ALL' || currentSubtopicFilter !== 'ALL';
        const weekLabel = currentWeekFilter !== 'ALL' ? currentWeekFilter : 'All Weeks';
        const sectionName = isSectionTest ? 
            (currentSubtopicFilter !== 'ALL' ? `${weekLabel} - ${currentSubtopicFilter}` : weekLabel) : 
            'Full Syllabus (All Weeks)';
        
        let sectionScore = 0;
        let sectionMaxMarks = 0;
        let sectionAttempted = 0;
        let sectionCorrect = 0;
        currentQuestions.forEach(q => {
            sectionMaxMarks += q.marks;
            const resp = responses[q.id];
            if (resp.evaluation && resp.evaluation.isAttempted) {
                sectionAttempted++;
                if (resp.evaluation.isCorrect) {
                    sectionCorrect++;
                    sectionScore += q.marks;
                }
            }
        });

        const activeAttempted = isSectionTest ? sectionAttempted : attemptedCount;
        const activeCorrect = isSectionTest ? sectionCorrect : correctCount;
        const activeScore = isSectionTest ? sectionScore : totalScore;
        const activeMax = isSectionTest ? sectionMaxMarks : maxMarks;
        const activeAccuracy = activeAttempted > 0 ? Math.round((activeCorrect / activeAttempted) * 100) : 0;

        // Record Test Attempt in Auth & Admin storage
        const Auth = getAuth();
        const Admin = getAdmin();
        if (Auth) {
            Auth.recordTestAttempt({
                section: sectionName,
                totalQuestions: isSectionTest ? currentQuestions.length : allQuestions.length,
                attempted: activeAttempted,
                correct: activeCorrect,
                score: activeScore,
                maxMarks: activeMax,
                accuracy: activeAccuracy,
                timeSpent: `${Math.round((180 * 60 - totalSeconds) / 60)} mins`
            });
            if (Admin) {
                Admin.renderOverview();
                Admin.renderAttemptsTable();
                Admin.renderUsersTable();
            }
        }

        // Render Metric Cards
        elements.resTotalScore.textContent = activeScore;
        elements.resMaxMarks.textContent = activeMax;
        elements.resAccuracy.textContent = `${activeAccuracy}%`;
        elements.resAttempted.textContent = activeAttempted;
        elements.resCorrect.textContent = activeCorrect;
        elements.resIncorrect.textContent = activeAttempted - activeCorrect;

        const subTitle = document.querySelector('#scorecardView .scorecard-header p');
        if (subTitle) {
            subTitle.textContent = `Modern Application Development 1 (MAD 1 / AppDev1) — ${sectionName} Examination Scorecard`;
        }

        // Render Scorecard Detailed Table
        renderScorecardTable(categoryStats);

        // Switch to Scorecard View
        elements.examInterfaceView.style.display = 'none';
        elements.scorecardView.style.display = 'block';
    }

    function renderScorecardTable(categoryStats) {
        elements.scorecardTableBody.innerHTML = '';
        allQuestions.forEach((q, idx) => {
            const resp = responses[q.id];
            const ev = resp.evaluation || { isAttempted: false, isCorrect: false, marksAwarded: 0 };
            
            const tr = document.createElement('tr');
            
            // Format student chosen answer
            let studentAnsText = '<span class="text-muted">Unattempted</span>';
            if (ev.isAttempted) {
                if (q.question_type === 'SA') {
                    studentAnsText = `<b>${resp.value}</b>`;
                } else {
                    const letters = resp.selectedOptions.map(optId => {
                        const optIndex = q.options.findIndex(o => o.option_id === optId);
                        return optIndex >= 0 ? String.fromCharCode(65 + optIndex) : optId;
                    });
                    studentAnsText = `Option (${letters.join(', ')})`;
                }
            }

            // Format official answer key
            let officialKeyText = 'N/A';
            if (q.correct_answer && q.correct_answer.length > 0) {
                if (q.question_type === 'SA') {
                    officialKeyText = `<b>${q.correct_answer.join(' or ')}</b>`;
                } else {
                    const correctLetters = q.correct_answer.map(optId => {
                        const optIndex = q.options.findIndex(o => o.option_id === optId);
                        return optIndex >= 0 ? String.fromCharCode(65 + optIndex) : optId;
                    });
                    officialKeyText = `<b>Option (${correctLetters.join(', ')})</b>`;
                }
            }

            tr.innerHTML = `
                <td><b>${q.id}</b></td>
                <td><small>${q.week.split(':')[0]}</small></td>
                <td><small>${q.subtopic}</small></td>
                <td><span class="badge ${q.question_type === 'MCQ' ? 'badge-info' : (q.question_type === 'MSQ' ? 'badge-warning' : 'badge-secondary')}">${q.question_type}</span></td>
                <td>${studentAnsText}</td>
                <td>${officialKeyText}</td>
                <td>
                    <span class="badge ${ev.isCorrect ? 'badge-success' : (ev.isAttempted ? 'badge-danger' : 'badge-secondary')}">
                        ${ev.isCorrect ? 'CORRECT' : (ev.isAttempted ? 'INCORRECT' : 'UNATTEMPTED')}
                    </span>
                </td>
                <td><b>+${ev.marksAwarded}</b> / ${q.marks}</td>
            `;
            elements.scorecardTableBody.appendChild(tr);
        });
    }

    // ==================== EVENT LISTENERS ====================
    function bindEvents() {
        // Section / Week Filter Tabs
        elements.sectionTabs.querySelectorAll('.sec-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                elements.sectionTabs.querySelectorAll('.sec-tab').forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                currentWeekFilter = tab.dataset.week;
                currentSubtopicFilter = 'ALL';
                buildSubtopicDropdown();
                applyFilter();
            });
        });

        // Subtopic Select Dropdown
        elements.subtopicSelect.addEventListener('change', (e) => {
            currentSubtopicFilter = e.target.value;
            applyFilter();
        });

        // Pause/Resume Timer
        elements.pauseTimerBtn.addEventListener('click', () => {
            isPaused = !isPaused;
            elements.pauseTimerBtn.textContent = isPaused ? 'Resume' : 'Pause';
            elements.pauseTimerBtn.classList.toggle('btn-warning', isPaused);
        });

        // Save & Next Button
        elements.btnSaveNext.addEventListener('click', () => {
            const q = currentQuestions[currentIndex];
            const resp = responses[q.id];
            
            const hasAns = (q.question_type === 'SA') ? 
                (resp.value && resp.value.trim() !== '') : 
                (resp.selectedOptions && resp.selectedOptions.length > 0);

            if (hasAns) {
                resp.status = 'ANSWERED';
            } else {
                resp.status = 'NOT_ANSWERED';
            }

            updateLegendCounters();
            updatePaletteButton(currentIndex);

            if (currentIndex < currentQuestions.length - 1) {
                navigateToQuestion(currentIndex + 1);
            }
        });

        // Mark for Review & Next Button
        elements.btnMarkReview.addEventListener('click', () => {
            const q = currentQuestions[currentIndex];
            const resp = responses[q.id];

            const hasAns = (q.question_type === 'SA') ? 
                (resp.value && resp.value.trim() !== '') : 
                (resp.selectedOptions && resp.selectedOptions.length > 0);

            if (hasAns) {
                resp.status = 'ANS_MARKED_REVIEW';
            } else {
                resp.status = 'MARKED_REVIEW';
            }

            updateLegendCounters();
            updatePaletteButton(currentIndex);

            if (currentIndex < currentQuestions.length - 1) {
                navigateToQuestion(currentIndex + 1);
            }
        });

        // Clear Response Button
        elements.btnClearResponse.addEventListener('click', () => {
            const q = currentQuestions[currentIndex];
            const resp = responses[q.id];

            resp.selectedOptions = [];
            resp.value = '';
            resp.status = 'NOT_ANSWERED';

            renderOptions(q, resp);
            updateLegendCounters();
            updatePaletteButton(currentIndex);
        });

        // Next & Previous Navigation
        elements.btnNext.addEventListener('click', () => {
            if (currentIndex < currentQuestions.length - 1) {
                navigateToQuestion(currentIndex + 1);
            }
        });

        elements.btnPrev.addEventListener('click', () => {
            if (currentIndex > 0) {
                navigateToQuestion(currentIndex - 1);
            }
        });

        // "🎲 Random Question" / "Quick Random Practice" Buttons
        if (elements.btnQuickRandom) {
            elements.btnQuickRandom.addEventListener('click', () => selectRandomQuestion());
        }
        if (elements.btnMetaRandom) {
            elements.btnMetaRandom.addEventListener('click', () => selectRandomQuestion());
        }
        if (elements.btnFooterRandom) {
            elements.btnFooterRandom.addEventListener('click', () => selectRandomQuestion());
        }

        // Image Zoom Controls
        if (elements.btnZoomIn) {
            elements.btnZoomIn.addEventListener('click', () => setZoom(currentZoom + 0.15));
        }
        if (elements.btnZoomOut) {
            elements.btnZoomOut.addEventListener('click', () => setZoom(currentZoom - 0.15));
        }
        if (elements.btnZoomReset) {
            elements.btnZoomReset.addEventListener('click', () => setZoom(1.0));
        }
        if (elements.btnZoomModal && elements.examImageModal) {
            elements.btnZoomModal.addEventListener('click', () => {
                const q = currentQuestions[currentIndex];
                if (q && q.card_image) {
                    elements.examImageModalImg.src = q.card_image;
                    elements.examImageModalTitle.textContent = `${q.id} — Visual Question Card (100% Full Resolution)`;
                    elements.examImageModal.style.display = 'flex';
                }
            });
        }
        if (elements.btnExamImageModalClose && elements.examImageModal) {
            elements.btnExamImageModalClose.addEventListener('click', () => {
                elements.examImageModal.style.display = 'none';
            });
            elements.examImageModal.addEventListener('click', (e) => {
                if (e.target === elements.examImageModal) {
                    elements.examImageModal.style.display = 'none';
                }
            });
        }
        window.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && elements.examImageModal && elements.examImageModal.style.display === 'flex') {
                elements.examImageModal.style.display = 'none';
            }
        });

        // Submit Examination
        elements.btnSubmitExam.addEventListener('click', () => {
            submitExam();
        });

        // Review Solutions Button
        elements.btnReviewSolutions.addEventListener('click', () => {
            elements.scorecardView.style.display = 'none';
            elements.examInterfaceView.style.display = 'block';
            navigateToQuestion(0);
        });

        // Retake Exam Button
        elements.btnRetakeExam.addEventListener('click', () => {
            if (confirm("Reset all answers and re-take the examination from the beginning?")) {
                resetExamState();
                elements.scorecardView.style.display = 'none';
                elements.examInterfaceView.style.display = 'block';
                startTimer();
            }
        });

        // Scorecard Admin Dashboard button
        if (elements.btnScorecardAdminDashboard) {
            elements.btnScorecardAdminDashboard.addEventListener('click', () => {
                elements.scorecardView.style.display = 'none';
                elements.adminDashboardView.style.display = 'block';
                elements.btnToggleAdminView.style.display = 'none';
                elements.btnToggleExamView.style.display = 'inline-block';
                const Admin = getAdmin();
                if (Admin) {
                    Admin.renderOverview();
                    Admin.renderUsersTable();
                    Admin.renderAttemptsTable();
                    Admin.renderQuestionsTable();
                    Admin.renderSyllabusAnalytics();
                }
            });
        }

        // ==================== AUTH MODAL HANDLERS ====================
        elements.tabLoginBtn.addEventListener('click', () => {
            elements.tabLoginBtn.classList.add('active');
            elements.tabSignupBtn.classList.remove('active');
            elements.formLogin.style.display = 'block';
            elements.formSignup.style.display = 'none';
            hideAuthAlert();
        });

        elements.tabSignupBtn.addEventListener('click', () => {
            elements.tabSignupBtn.classList.add('active');
            elements.tabLoginBtn.classList.remove('active');
            elements.formLogin.style.display = 'none';
            elements.formSignup.style.display = 'block';
            hideAuthAlert();
        });

        // Form Login
        elements.formLogin.addEventListener('submit', (e) => {
            e.preventDefault();
            const idVal = document.getElementById('loginIdentifier').value;
            const passVal = document.getElementById('loginPassword').value;
            const rememberMe = document.getElementById('loginRememberMe').checked;

            const Auth = getAuth();
            if (!Auth) {
                showAuthAlert('Authentication module failed to load.');
                return;
            }
            const res = Auth.login(idVal, passVal, rememberMe);
            if (res.success) {
                checkAuthAndSetupUI();
            } else {
                showAuthAlert(res.error || res.message || 'Login failed.');
            }
        });

        // Form Signup
        elements.formSignup.addEventListener('submit', (e) => {
            e.preventDefault();
            const name = document.getElementById('signupName').value;
            const email = document.getElementById('signupEmail').value;
            const rollNo = document.getElementById('signupRoll').value;
            const password = document.getElementById('signupPassword').value;
            const role = document.getElementById('signupRole').value;

            const Auth = getAuth();
            if (!Auth) {
                showAuthAlert('Authentication module failed to load.');
                return;
            }
            const res = Auth.signUp(name, email, rollNo, password, role);
            if (res.success) {
                checkAuthAndSetupUI();
            } else {
                showAuthAlert(res.error || res.message || 'Registration failed.');
            }
        });

        // Quick Demo Logins
        elements.btnQuickStudent.addEventListener('click', () => {
            document.getElementById('loginIdentifier').value = 'student@iitm.ac.in';
            document.getElementById('loginPassword').value = 'Student@123';
            const Auth = getAuth();
            if (Auth) {
                const res = Auth.login('student@iitm.ac.in', 'Student@123', true);
                if (res.success) checkAuthAndSetupUI();
                else showAuthAlert(res.error || res.message || 'Login failed.');
            }
        });

        elements.btnQuickAdmin.addEventListener('click', () => {
            document.getElementById('loginIdentifier').value = 'admin@iitm.ac.in';
            document.getElementById('loginPassword').value = 'Admin@123';
            const Auth = getAuth();
            if (Auth) {
                const res = Auth.login('admin@iitm.ac.in', 'Admin@123', true);
                if (res.success) checkAuthAndSetupUI();
                else showAuthAlert(res.error || res.message || 'Login failed.');
            }
        });

        // Logout
        elements.btnLogout.addEventListener('click', () => {
            if (confirm("Sign out of MAD 1 CBT portal?")) {
                const Auth = getAuth();
                if (Auth) Auth.logout();
                resetExamState();
                elements.authModal.style.display = 'flex';
                elements.btnToggleAdminView.style.display = 'none';
                elements.btnToggleExamView.style.display = 'none';
                elements.examInterfaceView.style.display = 'block';
                elements.adminDashboardView.style.display = 'none';
                elements.scorecardView.style.display = 'none';
            }
        });

        // Switch to Admin Dashboard View
        elements.btnToggleAdminView.addEventListener('click', () => {
            elements.examInterfaceView.style.display = 'none';
            elements.scorecardView.style.display = 'none';
            elements.adminDashboardView.style.display = 'block';
            elements.btnToggleAdminView.style.display = 'none';
            elements.btnToggleExamView.style.display = 'inline-block';
            const Admin = getAdmin();
            if (Admin) {
                Admin.renderOverview();
                Admin.renderUsersTable();
                Admin.renderAttemptsTable();
                Admin.renderQuestionsTable();
                Admin.renderSyllabusAnalytics();
            }
        });

        // Switch back to Exam View / Scorecard View
        elements.btnToggleExamView.addEventListener('click', () => {
            elements.adminDashboardView.style.display = 'none';
            elements.btnToggleExamView.style.display = 'none';
            const Auth = getAuth();
            const curUser = Auth ? Auth.getCurrentUser() : null;
            if (curUser && curUser.role === 'admin') {
                elements.btnToggleAdminView.style.display = 'inline-block';
            }

            if (isExamSubmitted) {
                elements.scorecardView.style.display = 'block';
                elements.examInterfaceView.style.display = 'none';
            } else {
                elements.examInterfaceView.style.display = 'block';
                elements.scorecardView.style.display = 'none';
                startTimer();
            }
        });
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
