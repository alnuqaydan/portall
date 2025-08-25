#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standalone test server for local development
Uses only Python standard library for testing without dependencies
"""

import json
import http.server
import socketserver
import os
from urllib.parse import urlparse, parse_qs

class HudHudHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path in ['/health', '/healthz']:
            self.send_health_response()
        elif parsed_path.path == '/':
            self.send_main_page()
        else:
            self.send_404()
    
    def send_health_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            'status': 'healthy',
            'service': 'Hudhud KPI System',
            'mode': 'standalone-test',
            'version': '1.0.0'
        }
        self.wfile.write(json.dumps(response).encode())
    
    def send_main_page(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Hudhud KPI System</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                .header { text-align: center; margin-bottom: 40px; }
                .status { background: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0; }
                .endpoint { background: #f8f9fa; padding: 10px; margin: 10px 0; border-left: 4px solid #007bff; }
                .code { font-family: monospace; background: #f1f3f4; padding: 2px 6px; border-radius: 3px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 Hudhud KPI System</h1>
                    <p>Dynamic KPI Monitoring System for Reviewers</p>
                </div>
                
                <div class="status">
                    <h3>✅ System Status: Running</h3>
                    <p><strong>Mode:</strong> Standalone Test Server</p>
                    <p><strong>Version:</strong> 1.0.0</p>
                    <p><strong>Environment:</strong> Development</p>
                </div>
                
                <div>
                    <h3>📡 Available Endpoints</h3>
                    <div class="endpoint">
                        <strong>Health Check:</strong> <span class="code">/health</span> and <span class="code">/healthz</span>
                    </div>
                    <div class="endpoint">
                        <strong>Main Dashboard:</strong> <span class="code">/</span>
                    </div>
                </div>
                
                <div style="margin-top: 40px; text-align: center; color: #666;">
                    <p>© 2024 Hudhud Team. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html.encode())
    
    def send_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {'error': 'Not found'}
        self.wfile.write(json.dumps(response).encode())

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8050))
    
    print(f"🚀 Starting Hudhud KPI System Test Server on port {port}")
    print(f"🌐 Access: http://localhost:{port}")
    print("📊 Mode: Standalone Test Server (Python standard library only)")
    print("\nAvailable endpoints:")
    print("  /        - Main dashboard")
    print("  /health  - Health check")
    print("  /healthz - Health check (Render compatible)")
    
    try:
        with socketserver.TCPServer(("", port), HudHudHandler) as httpd:
            print(f"\n✅ Server running successfully at http://localhost:{port}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")