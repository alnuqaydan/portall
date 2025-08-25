# Render Deployment Guide for Portall

## 🚀 Deployment Configuration

### Current Settings
- **Service Name**: portall
- **Region**: Frankfurt (EU Central)
- **Instance Type**: Starter (0.5 CPU, 512 MB)
- **Repository**: https://github.com/alnuqaydan/portall
- **Branch**: main
- **Health Check Path**: `/healthz`

### Build & Deploy Commands
- **Build Command**: `chmod +x build.sh && ./build.sh`
- **Start Command**: `gunicorn app:app --config gunicorn.conf.py`

## 📋 Pre-Deployment Checklist

### ✅ Code Changes Made
1. **Health Check Endpoints**: Added both `/health` and `/healthz` endpoints
2. **Gunicorn Configuration**: Optimized for Render's environment
3. **Build Script**: Created `build.sh` for efficient dependency installation
4. **Render Configuration**: Added `render.yaml` for infrastructure-as-code

### ✅ Files Added/Modified for Better Deployment
- `app.py` - Added Render health check endpoints (/health and /healthz)
- `gunicorn.conf.py` - Optimized for Render deployment
- `build.sh` - Build script for efficient dependency installation
- `render.yaml` - Infrastructure-as-code configuration
- `deploy_render.py` - Enhanced deployment validation with --skip-deps option
- `quick_deploy.sh` - Automated deployment script
- `requirements-minimal.txt` - Minimal dependencies for faster builds
- `test_deployment.py` - Test deployment configuration
- `check_deployment.py` - Monitor deployment health status
- `data/` - Created required directory structure

## 🔧 Deployment Steps

### Option A: Quick Deploy (Recommended)
```bash
# Validate and deploy in one command
./quick_deploy.sh

# Or with custom commit message
./quick_deploy.sh "Add new feature: improved KPI dashboard"

# Validate only (no deployment)
./quick_deploy.sh --validate-only
```

### Option B: Manual Deployment
1. **Validate Deployment Readiness**
   ```bash
   python deploy_render.py --skip-deps
   ```

2. **Commit and Push Changes**
   ```bash
   git add .
   git commit -m "Optimize for Render deployment"
   git push origin main
   ```

3. **Monitor Deployment**
   ```bash
   # Check deployment status
   python check_deployment.py
   
   # Continuous monitoring
   python check_deployment.py --monitor
   ```

### 4. Render Auto-Deploy
- Render will automatically detect changes and start deployment
- Monitor the deployment logs in Render dashboard

### 5. Verify Deployment
- Check health endpoint: `https://portall-nn5x.onrender.com/healthz`
- Monitor application logs for any errors
- Use deployment status checker for automated monitoring

## 🚨 Troubleshooting

### Common Issues

#### Build Failures
- **Dependency Issues**: Check `requirements.txt` for version conflicts
- **Memory Issues**: Render starter plan has 512MB limit
- **Timeout Issues**: Build command takes too long

#### Runtime Issues
- **Health Check Failures**: Verify `/healthz` endpoint is accessible
- **Memory Errors**: Monitor memory usage in Render dashboard
- **Startup Timeouts**: Check gunicorn configuration

### Debug Commands

#### Check Application Status
```bash
# Test health endpoint locally
curl http://localhost:8050/healthz

# Check gunicorn configuration
gunicorn --check-config app:app --config gunicorn.conf.py
```

#### Monitor Resources
```bash
# Check Python version
python --version

# Check installed packages
pip list

# Test imports
python -c "import dash, flask, gunicorn; print('OK')"
```

## 📊 Performance Optimization

### Render Starter Plan Limitations
- **CPU**: 0.5 cores (shared)
- **Memory**: 512 MB
- **Disk**: 1 GB
- **Network**: Limited bandwidth

### Optimization Strategies
1. **Worker Processes**: Limited to 4 workers
2. **Memory Management**: Use efficient data structures
3. **Caching**: Implement Redis or file-based caching
4. **Static Assets**: Use CDN for large files

## 🛠️ Deployment Tools

### 1. Quick Deploy Script (`./quick_deploy.sh`)
Automated deployment script that handles validation, Git operations, and provides deployment instructions.

```bash
# Quick deploy with auto-generated commit message
./quick_deploy.sh

# Deploy with custom commit message  
./quick_deploy.sh "Add new dashboard features"

# Validate only (no Git operations)
./quick_deploy.sh --validate-only

# Skip Git operations (for testing)
./quick_deploy.sh --no-git
```

### 2. Deployment Validator (`deploy_render.py`)
Validates deployment readiness with improved error handling.

```bash
# Full validation including dependency check
python deploy_render.py

# Fast validation (skip dependency installation)
python deploy_render.py --skip-deps
```

### 3. Deployment Status Checker (`check_deployment.py`)
Monitor your deployed application's health and performance.

```bash
# Single health check
python check_deployment.py

# Continuous monitoring (30s intervals)
python check_deployment.py --monitor

# Check local development server
python check_deployment.py --local

# Custom monitoring interval
python check_deployment.py --monitor --interval 60
```

### 4. Configuration Tester (`test_deployment.py`)
Test deployment configuration files and health endpoints.

```bash
# Test all deployment configurations
python test_deployment.py
```

### 5. Minimal Requirements (`requirements-minimal.txt`)
Use for faster development builds when testing deployment.

```bash
# Install minimal dependencies for testing
pip install -r requirements-minimal.txt
```

## 🔄 Auto-Deploy Configuration

### Triggers
- **On Commit**: Automatically deploy on main branch changes
- **Manual**: Use deploy hook for manual deployments

### Excluded Paths
- `.git/`
- `README.md`
- `*.log`
- `cache/`
- `logs/`

## 📈 Monitoring & Health Checks

### Health Check Endpoints
- **Primary**: `/healthz` (Render default)
- **Secondary**: `/health` (Application specific)

### Expected Response
```json
{
  "status": "healthy",
  "service": "Hudhud KPI System"
}
```

### Monitoring Metrics
- Response time
- Memory usage
- CPU usage
- Error rates

## 🆘 Support & Resources

### Render Documentation
- [Web Services](https://render.com/docs/web-services)
- [Health Checks](https://render.com/docs/health-checks)
- [Environment Variables](https://render.com/docs/environment-variables)

### Application Logs
- Access logs: Gunicorn access logs
- Error logs: Gunicorn error logs
- Application logs: Custom logging system

### Contact Information
- **Repository**: https://github.com/alnuqaydan/portall
- **Render Service**: https://dashboard.render.com/web/portall
- **Health URL**: https://portall-nn5x.onrender.com/healthz

## 🎯 Next Steps

1. **Deploy**: Push changes and monitor deployment
2. **Test**: Verify all endpoints work correctly
3. **Monitor**: Set up alerts for health check failures
4. **Optimize**: Monitor performance and optimize as needed
5. **Scale**: Consider upgrading plan if needed
