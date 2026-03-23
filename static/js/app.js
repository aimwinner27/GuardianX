const app = {
    currentUser: null,
    pollingIntervals: {},

    async init() {
        if(!localStorage.getItem('token')) {
            window.location.href = '/login';
            return;
        }

        try {
            this.currentUser = await api.getMe();
            document.getElementById('userInfo').textContent = `Hi, ${this.currentUser.register_or_name} (${this.currentUser.role})`;
            this.setupRoleAccess();
        } catch (e) {
            localStorage.removeItem('token');
            window.location.href = '/login';
        }

        document.getElementById('logoutBtn').addEventListener('click', () => {
            localStorage.removeItem('token');
            window.location.href = '/login';
        });

        // Setup Forms
        document.getElementById('gpForm')?.addEventListener('submit', this.handleGatePassSubmit.bind(this));
        document.getElementById('reportForm')?.addEventListener('submit', this.handleReportSubmit.bind(this));
    },

    setupRoleAccess() {
        // Hide certain cards/buttons based on role
        const role = this.currentUser.role;
        if(role === 'student') {
            document.getElementById('gp-form-container').style.display = 'block';
        } else {
            document.getElementById('gp-form-container').style.display = 'none';
        }
    },

    showSection(sectionId) {
        document.querySelectorAll('.module-section').forEach(s => s.classList.remove('active'));
        document.getElementById('mainDashboard').classList.remove('active');
        document.getElementById(sectionId).classList.add('active');

        // Stop all polling first
        Object.values(this.pollingIntervals).forEach(clearInterval);

        // Run section specific initializer logic
        if(sectionId === 'gatePassSection') this.loadGatePasses();
        if(sectionId === 'reportSection') this.loadReports();
        if(sectionId === 'crowdSection') {
            this.fetchCrowd();
            this.pollingIntervals.crowd = setInterval(() => this.fetchCrowd(), 2000);
        }
        if(sectionId === 'energySection') {
            this.fetchEnergy();
            this.pollingIntervals.energy = setInterval(() => this.fetchEnergy(), 3000);
        }
    },

    // --- GATE PASS ---
    async handleGatePassSubmit(e) {
        e.preventDefault();
        const data = {
            reason: document.getElementById('gpReason').value,
            out_time: document.getElementById('gpOutTime').value,
            expected_return_time: document.getElementById('gpReturnTime').value
        };
        await api.createPass(data);
        alert('Pass requested successfully!');
        e.target.reset();
        this.loadGatePasses();
    },

    async loadGatePasses() {
        const passes = await api.getPasses();
        const tbody = document.querySelector('#gpTable tbody');
        tbody.innerHTML = '';
        passes.forEach(p => {
            let actions = '';
            const role = this.currentUser.role;
            if (role === 'admin' && p.status === 'pending') {
                actions = `<button class="btn" style="padding: 0.25rem 0.5rem;" onclick="app.updatePass(${p.id}, 'approve')">Approve</button>
                           <button class="btn btn-danger" style="padding: 0.25rem 0.5rem;" onclick="app.updatePass(${p.id}, 'reject')">Reject</button>`;
            } else if (role === 'security' && p.status === 'approved') {
                actions = `<button class="btn btn-warning" style="padding: 0.25rem 0.5rem;" onclick="app.updatePass(${p.id}, 'scan_exit')">Scan Exit</button>`;
            } else if (role === 'security' && p.status === 'exited') {
                actions = `<button class="btn" style="padding: 0.25rem 0.5rem;" onclick="app.updatePass(${p.id}, 'scan_return')">Scan Return</button>`;
            }

            // Status Badge Colors
            let badgeClass = 'badge-pending';
            if(['approved', 'returned'].includes(p.status)) badgeClass = 'badge-approved';
            if(p.status === 'rejected') badgeClass = 'badge-rejected';
            if(p.status === 'exited') badgeClass = 'badge-critical';

            tbody.innerHTML += `
                <tr>
                    <td>${p.reason}</td>
                    <td><span class="badge ${badgeClass}">${p.status.toUpperCase()}</span></td>
                    <td>${actions || '-'}</td>
                </tr>
            `;
        });
    },

    async updatePass(id, action) {
        await api.updatePassStatus(id, action);
        this.loadGatePasses();
    },

    // --- REPORTS ---
    async handleReportSubmit(e) {
        e.preventDefault();
        const formData = new FormData();
        formData.append('description', document.getElementById('repDesc').value);
        formData.append('location', document.getElementById('repLoc').value);
        
        await api.createReport(formData);
        alert('Report submmited. Alert triggered based on urgency.');
        e.target.reset();
    },

    async loadReports() {
        if(this.currentUser.role === 'student') return; // Students shouldn't load all reports
        const reports = await api.getReports();
        const tbody = document.querySelector('#reportsTable tbody');
        tbody.innerHTML = '';
        reports.forEach(r => {
            let actBtn = r.status === 'open' ? `<button class="btn" style="padding:0.25rem" onclick="app.resolveRep(${r.id})">Resolve</button>` : 'Resolved';
            let priBadge = r.priority === 'critical' ? 'badge-critical' : (r.priority === 'high' ? 'badge-rejected' : 'badge-pending');
            tbody.innerHTML += `
                <tr>
                    <td>${r.description}</td>
                    <td>${r.location}</td>
                    <td><span class="badge ${priBadge}">${r.priority.toUpperCase()}</span></td>
                    <td>${actBtn}</td>
                </tr>
            `;
        });
    },

    async resolveRep(id) {
        await api.resolveReport(id);
        this.loadReports();
    },

    // --- CROWD ---
    async fetchCrowd() {
        const data = await api.getCrowdStatus();
        document.getElementById('crowdCountNode').textContent = data.count;
        document.getElementById('crowdStatusNode').textContent = `STATUS: ${data.status.toUpperCase()}`;
        
        let color = '#10B981';
        if(data.status === 'high') color = '#F59E0B';
        if(data.status === 'critical') color = '#EF4444';
        
        document.getElementById('crowdStatusNode').style.color = color;
        document.getElementById('crowdBbox').style.borderColor = color;
    },

    // --- ENERGY ---
    async fetchEnergy() {
        const data = await api.getEnergyStats();
        document.getElementById('energyTotalNode').textContent = `${data.total_usage_kwh} kWh`;
        
        const tbody = document.querySelector('#energyTable tbody');
        tbody.innerHTML = '';
        for (const [zone, usage] of Object.entries(data.zones)) {
            let warn = data.anomalies.includes(zone) ? '⚠️' : '';
            tbody.innerHTML += `<tr><td>${zone} ${warn}</td><td>${usage.toFixed(2)}</td></tr>`;
        }

        const warnNode = document.getElementById('energyAnomaliesNode');
        if(data.anomalies.length > 0) {
            warnNode.innerHTML = `<div class="glass-panel" style="background: rgba(239, 68, 68, 0.2); border-color: red;">
                <h3 style="color: #EF4444;">Wastage Alert</h3>
                <p>High consumption detected in: ${data.anomalies.join(', ')}</p>
            </div>`;
        } else {
            warnNode.innerHTML = '';
        }
    }
};

window.onload = () => {
    // Determine active page scope, if dashboard, init App
    if(document.getElementById('mainDashboard')) {
        app.init();
    }
};
