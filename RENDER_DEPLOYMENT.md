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

### ✅ Files Modified
- `app.py` - Added Render health check endpoint
- `gunicorn.conf.py` - Optimized for Render deployment
- `build.sh` - New build script
- `render.yaml` - Infrastructure configuration

## 🔧 Deployment Steps

### 1. Commit and Push Changes
```bash
git add .
git commit -m "Optimize for Render deployment"
git push origin main
```

### 2. Render Auto-Deploy
- Render will automatically detect changes and start deployment
- Monitor the deployment logs in Render dashboard

### 3. Verify Deployment
- Check health endpoint: `https://portall-nn5x.onrender.com/healthz`
- Monitor application logs for any errors

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
