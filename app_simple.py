#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hudhud KPI System - Simplified for deployment
"""

try:
    # Try to import the full application
    from app import app_instance
    app = app_instance.app
    full_app_available = True
except ImportError:
    # Fallback to minimal Flask app
    from flask import Flask, jsonify, render_template_string
    
    app = Flask(__name__)
    full_app_available = False
    
    # Simple HTML template for the main page
    MAIN_TEMPLATE = """
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
                <p><strong>Mode:</strong> {{ mode }}</p>
                <p><strong>Version:</strong> 1.0.0</p>
                <p><strong>Environment:</strong> Production</p>
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
    
    @app.route('/')
    def index():
        mode = "Full Application" if full_app_available else "Minimal Mode"
        return render_template_string(MAIN_TEMPLATE, mode=mode)
    
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'Hudhud KPI System',
            'mode': 'full' if full_app_available else 'minimal',
            'version': '1.0.0'
        }), 200
    
    @app.route('/healthz')
    def health_check_render():
        return jsonify({
            'status': 'healthy',
            'service': 'Hudhud KPI System',
            'mode': 'full' if full_app_available else 'minimal',
            'version': '1.0.0'
        }), 200

# This is what Gunicorn will look for
server = app.server if hasattr(app, 'server') else app

if __name__ == "__main__":
    port = 8050
    print(f"🚀 Starting Hudhud KPI System on port {port}")
    print(f"📊 Mode: {'Full Application' if full_app_available else 'Minimal Mode'}")
    print(f"🌐 Access: http://localhost:{port}")
    
    if hasattr(app, 'run_server'):
        # Dash app
        app.run_server(debug=False, host="0.0.0.0", port=port)
    else:
        # Flask app
        app.run(debug=False, host="0.0.0.0", port=port)