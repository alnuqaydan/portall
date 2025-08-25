#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gunicorn configuration for Hudhud KPI System
Production deployment configuration optimized for Render
"""

import os
import multiprocessing

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', '8050')}"
backlog = 2048

# Worker processes - simplified for deployment
workers = 1  # Use single worker for minimal setup
worker_class = 'sync'
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
preload_app = False  # Disabled to avoid import issues

# Timeouts
timeout = 120
keepalive = 2
graceful_timeout = 30

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = 'hudhud-kpi-system'

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Performance
max_requests_jitter = 50
worker_tmp_dir = '/dev/shm'
