#!/usr/bin/env node
/**
 * Hudhud KPI System - Node.js Implementation
 * Main entry point for the web application
 * 
 * Author: Hudhud Team
 * Date: 2024
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

class HudhudKPIServer {
    constructor(port = 8050) {
        this.port = port;
        this.server = http.createServer((req, res) => this.handleRequest(req, res));
    }

    handleRequest(req, res) {
        const parsedUrl = url.parse(req.url, true);
        const pathname = parsedUrl.pathname;

        // Set CORS headers
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
        res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

        if (req.method === 'OPTIONS') {
            res.writeHead(200);
            res.end();
            return;
        }

        if (pathname === '/' || pathname === '/index.html') {
            this.serveMainPage(res);
        } else if (pathname === '/api/data') {
            this.serveApiData(res);
        } else if (pathname === '/style.css') {
            this.serveStyles(res);
        } else {
            this.serve404(res);
        }
    }

    serveMainPage(res) {
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(this.getMainPageHTML());
    }

    serveApiData(res) {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        const data = this.loadCustomData();
        res.end(JSON.stringify(data));
    }

    serveStyles(res) {
        res.writeHead(200, { 'Content-Type': 'text/css' });
        res.end(this.getStyles());
    }

    serve404(res) {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('404 Not Found');
    }

    getMainPageHTML() {
        return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hudhud KPI System</title>
    <link rel="stylesheet" href="/style.css">
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>🏢 Hudhud KPI System</h1>
            <p>Field Survey Dashboard</p>
        </header>
        
        <main class="main-content">
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>Total Surveys</h3>
                    <div class="stat-value" id="total-surveys">-</div>
                </div>
                <div class="stat-card">
                    <h3>Approved</h3>
                    <div class="stat-value approved" id="approved-count">-</div>
                </div>
                <div class="stat-card">
                    <h3>Pending</h3>
                    <div class="stat-value pending" id="pending-count">-</div>
                </div>
                <div class="stat-card">
                    <h3>Rejected</h3>
                    <div class="stat-value rejected" id="rejected-count">-</div>
                </div>
            </div>
            
            <div class="data-section">
                <h2>Recent Surveys</h2>
                <div class="table-container">
                    <table id="data-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Name</th>
                                <th>City</th>
                                <th>Territory</th>
                                <th>Status</th>
                                <th>Date</th>
                                <th>Confidence</th>
                            </tr>
                        </thead>
                        <tbody id="table-body">
                            <tr><td colspan="7">Loading...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </main>
    </div>
    
    <script>
        // Load data when page loads
        window.addEventListener('load', loadData);
        
        async function loadData() {
            try {
                const response = await fetch('/api/data');
                const data = await response.json();
                updateStats(data);
                updateTable(data);
            } catch (error) {
                console.error('Error loading data:', error);
            }
        }
        
        function updateStats(data) {
            const total = data.length;
            const approved = data.filter(item => item.status === 'Approved').length;
            const pending = data.filter(item => item.status === 'Pending').length;
            const rejected = data.filter(item => item.status === 'Rejected').length;
            
            document.getElementById('total-surveys').textContent = total;
            document.getElementById('approved-count').textContent = approved;
            document.getElementById('pending-count').textContent = pending;
            document.getElementById('rejected-count').textContent = rejected;
        }
        
        function updateTable(data) {
            const tbody = document.getElementById('table-body');
            tbody.innerHTML = '';
            
            data.slice(0, 10).forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = \`
                    <td>\${item.id}</td>
                    <td>\${item.name}</td>
                    <td>\${item.city}</td>
                    <td>\${item.territory}</td>
                    <td><span class="status \${item.status.toLowerCase()}">\${item.status}</span></td>
                    <td>\${item.created_at}</td>
                    <td>\${(item.confidence * 100).toFixed(0)}%</td>
                \`;
                tbody.appendChild(row);
            });
        }
    </script>
</body>
</html>
        `;
    }

    getStyles() {
        return `
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Cairo', sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    color: #333;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.header {
    text-align: center;
    color: white;
    margin-bottom: 30px;
}

.header h1 {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 10px;
}

.header p {
    font-size: 1.2rem;
    opacity: 0.9;
}

.main-content {
    background: white;
    border-radius: 15px;
    padding: 30px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.stat-card {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    border-left: 4px solid #667eea;
}

.stat-card h3 {
    font-size: 0.9rem;
    color: #666;
    margin-bottom: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: #333;
}

.stat-value.approved {
    color: #28a745;
}

.stat-value.pending {
    color: #ffc107;
}

.stat-value.rejected {
    color: #dc3545;
}

.data-section h2 {
    margin-bottom: 20px;
    color: #333;
    font-weight: 600;
}

.table-container {
    overflow-x: auto;
    border-radius: 8px;
    border: 1px solid #e9ecef;
}

table {
    width: 100%;
    border-collapse: collapse;
    background: white;
}

th, td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #e9ecef;
}

th {
    background: #f8f9fa;
    font-weight: 600;
    color: #495057;
}

tr:hover {
    background: #f8f9fa;
}

.status {
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
}

.status.approved {
    background: #d4edda;
    color: #155724;
}

.status.pending {
    background: #fff3cd;
    color: #856404;
}

.status.rejected {
    background: #f8d7da;
    color: #721c24;
}

@media (max-width: 768px) {
    .container {
        padding: 10px;
    }
    
    .header h1 {
        font-size: 2rem;
    }
    
    .main-content {
        padding: 20px;
    }
    
    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 15px;
    }
}
        `;
    }

    generateSampleData() {
        const cities = ["Riyadh", "Jeddah", "Dammam", "Mecca", "Medina"];
        const territories = {
            "Riyadh": ["North", "South", "East", "West", "Central"],
            "Jeddah": ["North", "South", "East", "West"],
            "Dammam": ["North", "South", "East", "West"],
            "Mecca": ["Central", "Outer"],
            "Medina": ["Central", "Outer"]
        };
        
        const data = [];
        const startDate = new Date();
        startDate.setDate(startDate.getDate() - 30);
        
        for (let i = 0; i < 50; i++) {
            const city = cities[Math.floor(Math.random() * cities.length)];
            const territory = territories[city][Math.floor(Math.random() * territories[city].length)];
            const date = new Date(startDate.getTime() + Math.random() * 30 * 24 * 60 * 60 * 1000);
            
            data.push({
                id: i + 1,
                name: `Business ${i + 1}`,
                city: city,
                territory: territory,
                status: ["Pending", "Approved", "Rejected"][Math.floor(Math.random() * 3)],
                created_at: date.toISOString().split('T')[0],
                confidence: Math.round((Math.random() * 0.5 + 0.5) * 100) / 100,
                media_count: Math.floor(Math.random() * 6)
            });
        }
        
        return data;
    }

    loadCustomData() {
        try {
            // Try to read custom data file
            if (fs.existsSync('data.json')) {
                const fileContent = fs.readFileSync('data.json', 'utf8');
                const customData = JSON.parse(fileContent);
                console.log(`📊 Loaded ${customData.length} records from data.json`);
                return customData;
            } else {
                console.log('📝 data.json not found, using sample data');
                return this.generateSampleData();
            }
        } catch (error) {
            console.error('❌ Error loading custom data:', error.message);
            console.log('📝 Falling back to sample data');
            return this.generateSampleData();
        }
    }

    start() {
        this.server.listen(this.port, () => {
            console.log(`🚀 Hudhud KPI System running on port ${this.port}`);
            console.log(`📊 Dashboard available at: http://localhost:${this.port}`);
        });
    }
}

// Start the server
const port = process.env.PORT || 8050;
const server = new HudhudKPIServer(port);
server.start();