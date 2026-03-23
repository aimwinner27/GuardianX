const api = {
    baseUrl: '/api',

    // Helper for auth headers
    getHeaders() {
        const token = localStorage.getItem('token');
        const headers = {
            'Content-Type': 'application/json'
        };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        return headers;
    },

    async login(register_or_name, dob) {
        const response = await fetch(`${this.baseUrl}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ register_or_name, dob })
        });
        if(!response.ok) throw new Error("Invalid credentials");
        return response.json();
    },

    async getMe() {
        const response = await fetch(`${this.baseUrl}/auth/me`, {
            headers: this.getHeaders()
        });
        if(!response.ok) throw new Error("Not authenticated");
        return response.json();
    },

    // Gate Pass
    async createPass(data) {
        const response = await fetch(`${this.baseUrl}/passes/`, {
            method: 'POST',
            headers: this.getHeaders(),
            body: JSON.stringify(data)
        });
        return response.json();
    },
    
    async getPasses() {
        const response = await fetch(`${this.baseUrl}/passes/`, {
            headers: this.getHeaders()
        });
        return response.json();
    },

    async updatePassStatus(id, action) {
        // action: approve, reject, scan_exit, scan_return
        const response = await fetch(`${this.baseUrl}/passes/${id}/${action}`, {
            method: 'PUT',
            headers: this.getHeaders()
        });
        return response.json();
    },

    // Reports
    async createReport(formData) {
        // FormData doesn't need Content-Type header manually set, fetch does it
        const token = localStorage.getItem('token');
        const response = await fetch(`${this.baseUrl}/reports/`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` },
            body: formData
        });
        return response.json();
    },

    async getReports() {
        const response = await fetch(`${this.baseUrl}/reports/`, {
            headers: this.getHeaders()
        });
        return response.json();
    },
    
    async resolveReport(id) {
        const response = await fetch(`${this.baseUrl}/reports/${id}/resolve`, {
            method: 'PUT',
            headers: this.getHeaders()
        });
        return response.json();
    },

    // Analytics
    async getCrowdStatus() {
        const response = await fetch(`${this.baseUrl}/crowd/status`, {
            headers: this.getHeaders()
        });
        return response.json();
    },

    async getEnergyStats() {
        const response = await fetch(`${this.baseUrl}/energy/stats`, {
            headers: this.getHeaders()
        });
        return response.json();
    }
};
