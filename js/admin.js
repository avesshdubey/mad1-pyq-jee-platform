// Admin Control Panel & Dashboard Controller - MAD 1
(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        define(['MAD1Auth'], factory);
    } else if (typeof module === 'object' && module.exports) {
        module.exports = factory(require('./auth'));
    } else {
        root.MAD1Admin = factory(root.MAD1Auth || root.Auth);
        root.Admin = root.MAD1Admin;
        root.SCAdmin = root.MAD1Admin;
        root.MLTAdmin = root.MAD1Admin;
        root.MLFAdmin = root.MAD1Admin;
    }
}(typeof self !== 'undefined' ? self : this, function (Auth) {
    'use strict';

    let questionsData = [];

    const Admin = {
        init: function (questions) {
            questionsData = questions || window.MAD1_QUESTIONS || [];
            this.bindEvents();
            this.renderOverview();
            this.renderUsersTable();
            this.renderAttemptsTable();
            this.renderQuestionsTable();
            this.renderSyllabusAnalytics();
        },

        bindEvents: function () {
            // Admin Navigation Tabs
            document.querySelectorAll('.admin-nav-tab').forEach(tab => {
                tab.addEventListener('click', () => {
                    document.querySelectorAll('.admin-nav-tab').forEach(t => t.classList.remove('active'));
                    document.querySelectorAll('.admin-tab-content').forEach(c => c.style.display = 'none');
                    tab.classList.add('active');
                    const targetId = tab.dataset.tab;
                    const contentElem = document.getElementById(targetId);
                    if (contentElem) contentElem.style.display = 'block';

                    if (targetId === 'adminTabUsers') Admin.renderUsersTable();
                    if (targetId === 'adminTabAttempts') Admin.renderAttemptsTable();
                    if (targetId === 'adminTabQuestions') Admin.renderQuestionsTable();
                    if (targetId === 'adminTabAnalytics') Admin.renderSyllabusAnalytics();
                });
            });

            // User Search & Filter
            const userSearch = document.getElementById('adminUserSearch');
            if (userSearch) {
                userSearch.addEventListener('input', () => Admin.renderUsersTable());
            }
            const roleFilter = document.getElementById('adminUserRoleFilter');
            if (roleFilter) {
                roleFilter.addEventListener('change', () => Admin.renderUsersTable());
            }

            // Question Search & Filter
            const qSearch = document.getElementById('adminQuestionSearch');
            if (qSearch) {
                qSearch.addEventListener('input', () => Admin.renderQuestionsTable());
            }
            const qWeekFilter = document.getElementById('adminQuestionWeekFilter');
            if (qWeekFilter) {
                qWeekFilter.addEventListener('change', () => Admin.renderQuestionsTable());
            }
            const qTypeFilter = document.getElementById('adminQuestionTypeFilter');
            if (qTypeFilter) {
                qTypeFilter.addEventListener('change', () => Admin.renderQuestionsTable());
            }

            // Add Candidate User Modal Trigger
            const btnAddUser = document.getElementById('adminBtnAddUser');
            const addUserModal = document.getElementById('adminAddUserModal');
            const btnCloseAddUser = document.getElementById('adminBtnCloseAddUserModal');
            const formAddUser = document.getElementById('adminFormAddUser');

            if (btnAddUser && addUserModal) {
                btnAddUser.addEventListener('click', () => {
                    addUserModal.style.display = 'flex';
                });
            }
            if (btnCloseAddUser && addUserModal) {
                btnCloseAddUser.addEventListener('click', () => {
                    addUserModal.style.display = 'none';
                });
            }
            if (formAddUser) {
                formAddUser.addEventListener('submit', (e) => {
                    e.preventDefault();
                    const name = document.getElementById('adminNewUserName').value.trim();
                    const email = document.getElementById('adminNewUserEmail').value.trim();
                    const roll = document.getElementById('adminNewUserRoll').value.trim();
                    const pass = document.getElementById('adminNewUserPass').value.trim();
                    const role = document.getElementById('adminNewUserRole').value;

                    const res = Auth.signUp(name, email, roll, pass, role);
                    if (res.success) {
                        alert(`Candidate ${name} (${res.user.rollNo}) successfully added!`);
                        formAddUser.reset();
                        if (addUserModal) addUserModal.style.display = 'none';
                        Admin.renderUsersTable();
                        Admin.renderOverview();
                    } else {
                        alert(res.error || res.message || 'Failed to add candidate.');
                    }
                });
            }

            // Export Actions
            const btnExportJson = document.getElementById('adminBtnExportJson');
            if (btnExportJson) {
                btnExportJson.addEventListener('click', () => Admin.exportDataJson());
            }
            const btnExportCsv = document.getElementById('adminBtnExportCsv');
            if (btnExportCsv) {
                btnExportCsv.addEventListener('click', () => Admin.exportAttemptsCsv());
            }

            // Clear Attempts Action
            const btnClearAttempts = document.getElementById('adminBtnClearAttempts');
            if (btnClearAttempts) {
                btnClearAttempts.addEventListener('click', () => {
                    if (confirm('Are you sure you want to purge all test submission logs? This action is irreversible.')) {
                        Auth.clearAttempts();
                        Admin.renderAttemptsTable();
                        Admin.renderOverview();
                        alert('All exam submissions purged.');
                    }
                });
            }

            // Modal Preview Close
            const cardModal = document.getElementById('adminCardPreviewModal');
            const btnCloseCardModal = document.getElementById('adminBtnCloseCardPreview');
            if (btnCloseCardModal && cardModal) {
                btnCloseCardModal.addEventListener('click', () => {
                    cardModal.style.display = 'none';
                });
            }
        },

        renderOverview: function () {
            const users = Auth.getAllUsers();
            const attempts = Auth.getAttempts();
            const qs = questionsData.length ? questionsData : (window.MAD1_QUESTIONS || []);

            const countTotalQuestions = document.getElementById('adminMetricTotalQuestions');
            if (countTotalQuestions) countTotalQuestions.textContent = qs.length;

            const countTotalUsers = document.getElementById('adminMetricTotalUsers');
            if (countTotalUsers) countTotalUsers.textContent = users.length;

            const countTotalAttempts = document.getElementById('adminMetricTotalAttempts');
            if (countTotalAttempts) countTotalAttempts.textContent = attempts.length;

            let avgAccuracy = 0;
            if (attempts.length > 0) {
                const sumAcc = attempts.reduce((acc, cur) => acc + (parseFloat(cur.accuracy) || 0), 0);
                avgAccuracy = Math.round(sumAcc / attempts.length);
            }
            const metricAvgAcc = document.getElementById('adminMetricAvgAccuracy');
            if (metricAvgAcc) metricAvgAcc.textContent = `${avgAccuracy}%`;

            // Recent Submissions preview table (first 5)
            const recentBody = document.getElementById('adminRecentAttemptsTableBody');
            if (recentBody) {
                const recents = attempts.slice(0, 5);
                if (recents.length === 0) {
                    recentBody.innerHTML = `<tr><td colspan="7" class="text-center text-muted">No candidate attempts recorded yet.</td></tr>`;
                } else {
                    recentBody.innerHTML = recents.map(att => `
                        <tr>
                            <td><b>${att.id}</b></td>
                            <td>${att.userName} <span class="badge badge-subtle">${att.userRoll || ''}</span></td>
                            <td>${att.section}</td>
                            <td><span class="badge ${att.accuracy >= 70 ? 'badge-success' : (att.accuracy >= 40 ? 'badge-warning' : 'badge-danger')}">${att.score} / ${att.maxMarks}</span></td>
                            <td>${att.accuracy}%</td>
                            <td>${att.timeSpent || 'N/A'}</td>
                            <td><small>${new Date(att.timestamp).toLocaleDateString()} ${new Date(att.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</small></td>
                        </tr>
                    `).join('');
                }
            }
        },

        renderUsersTable: function () {
            const tbody = document.getElementById('adminUsersTableBody');
            if (!tbody) return;

            const users = Auth.getAllUsers();
            const searchVal = (document.getElementById('adminUserSearch')?.value || '').toLowerCase().trim();
            const roleVal = document.getElementById('adminUserRoleFilter')?.value || 'ALL';

            const filtered = users.filter(u => {
                const matchRole = roleVal === 'ALL' || u.role === roleVal;
                const matchSearch = !searchVal || 
                    u.name.toLowerCase().includes(searchVal) || 
                    u.email.toLowerCase().includes(searchVal) || 
                    (u.rollNo && u.rollNo.toLowerCase().includes(searchVal));
                return matchRole && matchSearch;
            });

            if (filtered.length === 0) {
                tbody.innerHTML = `<tr><td colspan="8" class="text-center text-muted">No candidate records match filter criteria.</td></tr>`;
                return;
            }

            tbody.innerHTML = filtered.map(u => `
                <tr>
                    <td><b>${u.rollNo || 'N/A'}</b></td>
                    <td>${u.name}</td>
                    <td>${u.email}</td>
                    <td><span class="badge ${u.role === 'admin' ? 'badge-role-admin' : 'badge-role-student'}">${u.role.toUpperCase()}</span></td>
                    <td><span class="badge ${u.status === 'active' ? 'badge-success' : 'badge-danger'}">${(u.status || 'active').toUpperCase()}</span></td>
                    <td>${u.testsTaken || 0}</td>
                    <td><b>${u.bestScore || 0} pts</b></td>
                    <td>
                        <button class="btn btn-sm btn-outline" onclick="window.MAD1Admin.promptResetPassword('${u.id}')">Reset Pass</button>
                        ${u.id !== 'usr_admin_01' ? `
                            <button class="btn btn-sm btn-outline-danger" onclick="window.MAD1Admin.confirmDeleteUser('${u.id}', '${u.name}')">Delete</button>
                        ` : ''}
                    </td>
                </tr>
            `).join('');
        },

        renderAttemptsTable: function () {
            const tbody = document.getElementById('adminAttemptsTableBody');
            if (!tbody) return;

            const attempts = Auth.getAttempts();
            if (attempts.length === 0) {
                tbody.innerHTML = `<tr><td colspan="8" class="text-center text-muted">No exam submissions recorded.</td></tr>`;
                return;
            }

            tbody.innerHTML = attempts.map(att => `
                <tr>
                    <td><b>${att.id}</b></td>
                    <td>${att.userName} <span class="badge badge-subtle">${att.userRoll || ''}</span></td>
                    <td>${att.section}</td>
                    <td>${att.attempted} / ${att.totalQuestions}</td>
                    <td><span class="badge ${att.score > 0 ? 'badge-success' : 'badge-secondary'}">${att.score} / ${att.maxMarks}</span></td>
                    <td><b>${att.accuracy}%</b></td>
                    <td>${att.timeSpent || 'N/A'}</td>
                    <td><small>${new Date(att.timestamp).toLocaleString()}</small></td>
                </tr>
            `).join('');
        },

        renderQuestionsTable: function () {
            const tbody = document.getElementById('adminQuestionsTableBody');
            if (!tbody) return;

            const qs = questionsData.length ? questionsData : (window.MAD1_QUESTIONS || []);
            const searchVal = (document.getElementById('adminQuestionSearch')?.value || '').toLowerCase().trim();
            const weekVal = document.getElementById('adminQuestionWeekFilter')?.value || 'ALL';
            const typeVal = document.getElementById('adminQuestionTypeFilter')?.value || 'ALL';

            const filtered = qs.filter(q => {
                const matchWeek = weekVal === 'ALL' || q.week.startsWith(weekVal);
                const matchType = typeVal === 'ALL' || q.question_type === typeVal;
                const matchSearch = !searchVal || 
                    q.id.toLowerCase().includes(searchVal) ||
                    (q.raw_q_id && q.raw_q_id.includes(searchVal)) ||
                    (q.subtopic && q.subtopic.toLowerCase().includes(searchVal)) ||
                    (q.question_text && q.question_text.toLowerCase().includes(searchVal));
                return matchWeek && matchType && matchSearch;
            });

            const countEl = document.getElementById('adminQuestionFilterCount');
            if (countEl) countEl.textContent = `Showing ${filtered.length} of ${qs.length} questions`;

            if (filtered.length === 0) {
                tbody.innerHTML = `<tr><td colspan="7" class="text-center text-muted">No questions match filter query.</td></tr>`;
                return;
            }

            tbody.innerHTML = filtered.slice(0, 50).map(q => `
                <tr>
                    <td><b>${q.id}</b></td>
                    <td><span class="badge badge-subtle">${q.week.split(':')[0]}</span></td>
                    <td><small>${q.subtopic}</small></td>
                    <td><span class="badge ${q.question_type === 'MCQ' ? 'badge-info' : (q.question_type === 'MSQ' ? 'badge-warning' : 'badge-secondary')}">${q.question_type}</span></td>
                    <td>+${q.marks}</td>
                    <td>
                        <button class="btn btn-sm btn-outline" onclick="window.MAD1Admin.previewCard('${q.card_image}', '${q.id}')">View Card</button>
                    </td>
                    <td><code>${q.correct_answer ? q.correct_answer.join(', ') : 'N/A'}</code></td>
                </tr>
            `).join('');
        },

        previewCard: function (cardRel, qId) {
            const modal = document.getElementById('adminCardPreviewModal');
            const img = document.getElementById('adminCardPreviewImg');
            const title = document.getElementById('adminCardPreviewTitle');
            if (modal && img) {
                img.src = cardRel;
                if (title) title.textContent = `Visual Question Card: ${qId}`;
                modal.style.display = 'flex';
            }
        },

        renderSyllabusAnalytics: function () {
            const container = document.getElementById('adminSyllabusChartContainer');
            if (!container) return;

            const qs = questionsData.length ? questionsData : (window.MAD1_QUESTIONS || []);
            const weekStats = {
                'Week 1: Internet Architecture & HTTP': 0,
                'Week 2: HTML5 & CSS3': 0,
                'Week 3: Flask & Routing': 0,
                'Week 4: Jinja2 & SQLite': 0
            };

            qs.forEach(q => {
                if (q.week.startsWith('Week 1')) weekStats['Week 1: Internet Architecture & HTTP']++;
                else if (q.week.startsWith('Week 2')) weekStats['Week 2: HTML5 & CSS3']++;
                else if (q.week.startsWith('Week 3')) weekStats['Week 3: Flask & Routing']++;
                else if (q.week.startsWith('Week 4')) weekStats['Week 4: Jinja2 & SQLite']++;
            });

            const maxCount = Math.max(...Object.values(weekStats), 1);

            container.innerHTML = `
                <div class="analytics-chart-grid">
                    ${Object.entries(weekStats).map(([w, count]) => `
                        <div class="analytics-bar-row">
                            <div class="analytics-bar-label"><b>${w}</b> (${count} Qs)</div>
                            <div class="analytics-bar-track">
                                <div class="analytics-bar-fill" style="width: ${Math.round((count / maxCount) * 100)}%;"></div>
                            </div>
                            <div class="analytics-bar-pct">${Math.round((count / qs.length) * 100)}%</div>
                        </div>
                    `).join('')}
                </div>
            `;
        },

        promptResetPassword: function (userId) {
            const newPass = prompt('Enter new password for this candidate (minimum 6 characters):', 'Student@123');
            if (newPass) {
                if (newPass.length < 6) {
                    alert('Password must be at least 6 characters long.');
                    return;
                }
                const res = Auth.resetPassword(userId, newPass);
                if (res.success) alert('Password updated successfully.');
                else alert(res.error || res.message || 'Failed to update password.');
            }
        },

        confirmDeleteUser: function (userId, name) {
            if (confirm(`Are you sure you want to remove candidate "${name}"? All associated attempt history will remain in archive.`)) {
                const res = Auth.deleteUser(userId);
                if (res.success) {
                    Admin.renderUsersTable();
                    Admin.renderOverview();
                } else {
                    alert(res.error || res.message || 'Cannot delete candidate.');
                }
            }
        },

        exportDataJson: function () {
            const data = {
                exportedAt: new Date().toISOString(),
                questions: questionsData.length ? questionsData : (window.MAD1_QUESTIONS || []),
                users: Auth.getAllUsers(),
                attempts: Auth.getAttempts()
            };
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `mad1_pyq_export_${Date.now()}.json`;
            a.click();
            URL.revokeObjectURL(url);
        },

        exportAttemptsCsv: function () {
            const attempts = Auth.getAttempts();
            if (attempts.length === 0) {
                alert('No test attempts to export.');
                return;
            }
            const headers = ['Attempt ID', 'Roll No', 'Name', 'Section', 'Score', 'Max Marks', 'Accuracy (%)', 'Questions Attempted', 'Total Questions', 'Time Spent', 'Timestamp'];
            const rows = attempts.map(a => [
                a.id,
                `"${a.userRoll || ''}"`,
                `"${a.userName || ''}"`,
                `"${a.section || ''}"`,
                a.score,
                a.maxMarks,
                a.accuracy,
                a.attempted,
                a.totalQuestions,
                `"${a.timeSpent || ''}"`,
                `"${a.timestamp || ''}"`
            ]);
            const csvContent = [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
            const blob = new Blob([csvContent], { type: 'text/csv' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `mad1_test_submissions_${Date.now()}.csv`;
            a.click();
            URL.revokeObjectURL(url);
        }
    };

    return Admin;
}));
