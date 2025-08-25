# 🚀 Deployment Guide

Quick reference for deploying the Hudhud KPI System.

## Quick Start

### 1. Validate Deployment
```bash
python deploy_render.py --skip-deps
```

### 2. Deploy (Automated)
```bash
./quick_deploy.sh
```

### 3. Monitor Deployment
```bash
python check_deployment.py
```

## Available Scripts

| Script | Purpose | Usage |
|--------|---------|--------|
| `quick_deploy.sh` | Automated deployment | `./quick_deploy.sh` |
| `deploy_render.py` | Validate deployment readiness | `python deploy_render.py --skip-deps` |
| `test_deployment.py` | Test configuration files | `python test_deployment.py` |
| `check_deployment.py` | Monitor deployment health | `python check_deployment.py --monitor` |

## Requirements Files

| File | Purpose | When to Use |
|------|---------|-------------|
| `requirements.txt` | Full dependencies | Production deployment |
| `requirements-minimal.txt` | Core dependencies only | Quick testing/development |

## Key Files

- `render.yaml` - Render platform configuration
- `Procfile` - Process definition for deployment
- `gunicorn.conf.py` - Production server configuration
- `app.py` - Main application with health endpoints

## Health Endpoints

- `/health` - Application health check
- `/healthz` - Render-compatible health check

## Troubleshooting

### Deployment Validation Fails
```bash
# Skip dependency check if network issues
python deploy_render.py --skip-deps
```

### Network Timeouts During Build
Use minimal requirements for testing:
```bash
pip install -r requirements-minimal.txt
```

### Check Deployment Status
```bash
# Monitor continuously
python check_deployment.py --monitor --interval 30
```

## Support

For detailed instructions, see:
- `RENDER_DEPLOYMENT.md` - Complete deployment guide
- `DEPLOYMENT_CHECKLIST.md` - Step-by-step checklist