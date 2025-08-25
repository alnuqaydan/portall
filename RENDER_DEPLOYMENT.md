# 🚀 Deploy Hudhud KPI System on Render

This guide will walk you through deploying the Hudhud KPI System on Render, a modern cloud platform for hosting web applications.

## 📋 Prerequisites

- **Render Account**: Sign up at [render.com](https://render.com)
- **Git Repository**: Your code should be in a Git repository (GitHub, GitLab, etc.)
- **Python Knowledge**: Basic understanding of Python web applications

## 🚀 Quick Deployment

### Step 1: Prepare Your Repository

Ensure your repository contains these essential files:

```
portal/
├── app.py                 # Main application
├── requirements.txt       # Python dependencies
├── render.yaml           # Render configuration
├── gunicorn.conf.py      # Gunicorn configuration
├── Procfile              # Process definition
├── hudhud/               # Core system modules
└── data/                 # Data directories
```

### Step 2: Connect Repository to Render

1. **Log into Render Dashboard**
   - Go to [dashboard.render.com](https://dashboard.render.com)
   - Sign in with your account

2. **Create New Web Service**
   - Click "New +" button
   - Select "Web Service"
   - Connect your Git repository

3. **Configure Service**
   - **Name**: `hudhud-kpi-system`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app.server --bind 0.0.0.0:$PORT`

### Step 3: Environment Variables

Set these environment variables in Render:

#### **Required Variables**
```bash
PORT=8050
DEBUG=false
LOG_LEVEL=INFO
CACHE_ENABLED=true
CACHE_TYPE=file
```

#### **Application Configuration**
```bash
REVIEWERS=malngedan,aalbwardi,fahad,naif
STARRED_USERS=malngedan,aalbwardi
DEFAULT_CITY=Riyadh
DEFAULT_TERRITORY=Central
SUPPORTED_CITIES=Riyadh,Jeddah,Dammam,Mecca,Medina
```

#### **Performance Settings**
```bash
WORKER_PROCESSES=4
MAX_CONNECTIONS=100
CONNECTION_TIMEOUT=30
QUERY_TIMEOUT=60
```

#### **Security Settings**
```bash
SECRET_KEY=your-secure-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600
```

### Step 4: Deploy

1. **Click "Create Web Service"**
2. **Wait for Build**: Render will automatically build and deploy your application
3. **Monitor Logs**: Check the build and runtime logs for any issues
4. **Access Your App**: Once deployed, you'll get a URL like `https://hudhud-kpi-system.onrender.com`

## 🔧 Advanced Configuration

### Using render.yaml (Recommended)

If you have the `render.yaml` file in your repository:

1. **Enable Blueprint Deployments**
   - Go to your Render dashboard
   - Click "Blueprints" in the left sidebar
   - Click "New Blueprint Instance"
   - Connect your repository
   - Render will automatically detect and use the `render.yaml`

2. **Automatic Configuration**
   - Environment variables are automatically set
   - Health checks are configured
   - Disk storage is provisioned

### Manual Configuration

If not using `render.yaml`:

1. **Build & Deploy Settings**
   ```
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app.server --bind 0.0.0.0:$PORT
   ```

2. **Health Check Path**
   ```
   Health Check Path: /health
   ```

3. **Auto-Deploy**
   - Enable "Auto-Deploy" for automatic updates
   - Set branch to `main` or `master`

## 📊 Monitoring & Health Checks

### Health Check Endpoint

Your application includes a health check endpoint at `/health`:

```bash
curl https://your-app.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Hudhud KPI System"
}
```

### Render Dashboard Monitoring

- **Logs**: Real-time application logs
- **Metrics**: CPU, memory, and request statistics
- **Deployments**: Build and deployment history
- **Health Status**: Service health monitoring

## 🗄️ Data Persistence

### Render Disk Storage

The `render.yaml` configures persistent disk storage:

```yaml
disk:
  name: hudhud-data
  mountPath: /app/data
  sizeGB: 1
```

This ensures your data persists across deployments.

### Data Directory Structure

```
/app/data/
├── input/            # Raw data files
├── cache/            # Processed data cache
├── output/           # Generated reports
├── exports/          # User exports
└── logs/             # Application logs
```

## 🔒 Security Considerations

### Environment Variables

- **Never commit secrets** to your repository
- **Use Render's environment variables** for sensitive data
- **Rotate secrets regularly**

### HTTPS & SSL

- **Automatic SSL**: Render provides free SSL certificates
- **HTTPS Only**: All traffic is automatically secured
- **Custom Domains**: Add your own domain with SSL

## 🚀 Performance Optimization

### Gunicorn Configuration

The `gunicorn.conf.py` optimizes for production:

- **Worker Processes**: Automatically scales based on CPU cores
- **Connection Pooling**: Efficient connection management
- **Request Limits**: Prevents abuse and ensures stability

### Caching Strategy

- **File-based Caching**: Persistent across deployments
- **Memory Optimization**: Efficient data structures
- **Background Processing**: Non-blocking operations

## 🐛 Troubleshooting

### Common Issues

#### 1. Build Failures

```bash
# Check requirements.txt
pip install -r requirements.txt

# Verify Python version
python --version
```

#### 2. Runtime Errors

```bash
# Check application logs in Render dashboard
# Verify environment variables are set correctly
# Test locally with same configuration
```

#### 3. Health Check Failures

```bash
# Ensure /health endpoint is accessible
# Check if application is binding to correct port
# Verify PORT environment variable
```

### Debug Mode

For troubleshooting, temporarily enable debug mode:

```bash
DEBUG=true
LOG_LEVEL=DEBUG
```

**Remember to disable debug mode in production!**

## 📈 Scaling

### Automatic Scaling

Render automatically scales your application based on:

- **Traffic patterns**
- **Resource usage**
- **Health check status**

### Manual Scaling

- **Instance Count**: Adjust number of instances
- **Resource Allocation**: Modify CPU and memory limits
- **Custom Domains**: Add multiple domains

## 🔄 Continuous Deployment

### Automatic Deployments

1. **Push to Main Branch**: Automatically triggers deployment
2. **Build Verification**: Render validates your code
3. **Health Check**: Ensures deployment success
4. **Rollback**: Automatic rollback on failures

### Deployment Strategies

- **Blue-Green**: Zero-downtime deployments
- **Rolling Updates**: Gradual traffic migration
- **Canary Deployments**: Test with subset of users

## 💰 Cost Optimization

### Render Plans

- **Starter**: $7/month - Good for development
- **Standard**: $25/month - Production ready
- **Pro**: $50/month - High performance

### Resource Optimization

- **Right-size instances**: Match resources to actual usage
- **Efficient caching**: Reduce database calls
- **Background jobs**: Use Render's background workers

## 📞 Support

### Render Support

- **Documentation**: [docs.render.com](https://docs.render.com)
- **Community**: [community.render.com](https://community.render.com)
- **Email Support**: Available on paid plans

### Application Support

- **Logs**: Check Render dashboard logs
- **Health Checks**: Monitor `/health` endpoint
- **Metrics**: Use Render's built-in monitoring

## 🎯 Next Steps

After successful deployment:

1. **Test Your Application**: Verify all features work correctly
2. **Monitor Performance**: Use Render's built-in metrics
3. **Set Up Alerts**: Configure notifications for issues
4. **Custom Domain**: Add your own domain name
5. **SSL Certificate**: Verify HTTPS is working
6. **Backup Strategy**: Implement data backup procedures

---

**Your Hudhud KPI System is now running in the cloud! 🚀**

For additional help, check the main `README.md` and `STARTUP_GUIDE.md` files.
