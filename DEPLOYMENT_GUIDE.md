# 🚀 RAGSPRO Deployment Guide

## Quick Deploy to Render (Recommended)

### Prerequisites
- GitHub account with repo: https://github.com/raghavshahhh/lead-genrater.git
- Render account (free): https://render.com

### Step 1: Push Docker Files to GitHub
```bash
git add .
git commit -m "Add Docker and Render deployment configuration"
git push origin main
```

### Step 2: Deploy on Render
1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository: `raghavshahhh/lead-genrater`
4. Render will auto-detect `render.yaml` and deploy automatically!
5. Wait 5-10 minutes for build to complete
6. Your dashboard will be live at: `https://ragspro-dashboard.onrender.com`

### Step 3: Configure Environment Variables (Optional)
In Render Dashboard → Your Service → Environment:
- `SERPAPI_KEY` - Your SerpAPI key for lead generation
- `GEMINI_API_KEY` - Your Google Gemini API key for AI content
- `FLASK_ENV` - Already set to `production`
- `PORT` - Already set to `5002`

---

## Local Docker Testing

### Test Docker Build Locally
```bash
# Run the deployment script
./deploy.sh
```

This will:
1. Build Docker image
2. Start container on port 5002
3. Test the deployment locally

### Manual Docker Commands
```bash
# Build image
docker build -t ragspro-dashboard:latest .

# Run container
docker run -d -p 5002:5002 --name ragspro ragspro-dashboard:latest

# View logs
docker logs ragspro

# Stop container
docker stop ragspro

# Remove container
docker rm ragspro
```

---

## Files Created for Deployment

### 1. `Dockerfile`
- Base image: Python 3.11 slim
- Installs system dependencies (wkhtmltopdf for PDF generation)
- Installs Python dependencies from requirements.txt
- Runs with Gunicorn (production server)
- Workers: 3, Timeout: 120s

### 2. `render.yaml`
- Service type: Web
- Environment: Docker
- Plan: Free tier
- Auto-deploy: Enabled on push to main branch
- Health check: Enabled

### 3. `.dockerignore`
- Excludes unnecessary files from Docker image
- Reduces image size
- Keeps sensitive data out

### 4. `deploy.sh`
- Automated deployment script
- Tests Docker build locally
- Provides step-by-step instructions

---

## Production Checklist

✅ **Completed:**
- [x] Dashboard uses PORT environment variable
- [x] requirements.txt with all dependencies
- [x] Dockerfile with wkhtmltopdf support
- [x] render.yaml configuration
- [x] .dockerignore for optimization
- [x] Gunicorn production server
- [x] All API endpoints working
- [x] Bulk export features (Excel, PDF, CSV)
- [x] Real-time lead generation
- [x] Dark theme RAGSPRO dashboard

🔧 **Optional Enhancements:**
- [ ] Add Redis for caching (if needed)
- [ ] Add PostgreSQL database (currently using JSON files)
- [ ] Add monitoring/logging service
- [ ] Add custom domain
- [ ] Add SSL certificate (Render provides free SSL)

---

## Troubleshooting

### Build Fails
- Check Docker logs: `docker logs ragspro`
- Verify all dependencies in requirements.txt
- Ensure Python 3.11 compatibility

### Port Issues
- Render automatically assigns PORT env var
- Dashboard.py already configured to use PORT env var
- Default fallback: 5002

### PDF Export Not Working
- wkhtmltopdf is installed in Dockerfile
- System dependencies included (libxrender1, libfontconfig1, etc.)
- If issues persist, check Render logs

### Database/Data Persistence
- Current setup uses JSON files in `data/` folder
- Data persists in container but resets on redeploy
- For production, consider PostgreSQL or persistent volume

---

## Architecture

```
User Browser
    ↓
Render Load Balancer (HTTPS)
    ↓
Docker Container (Port 5002)
    ↓
Gunicorn (3 workers)
    ↓
Flask App (dashboard.py)
    ↓
Backend (dashboard_ragspro.py)
    ↓
Data Storage (JSON files)
```

---

## Support

- **Dashboard URL (local):** http://localhost:5002
- **Dashboard URL (production):** https://ragspro-dashboard.onrender.com
- **GitHub Repo:** https://github.com/raghavshahhh/lead-genrater.git
- **Render Dashboard:** https://dashboard.render.com

---

## Next Steps After Deployment

1. **Test all features** on production URL
2. **Configure API keys** in Render environment variables
3. **Monitor logs** for any errors
4. **Set up custom domain** (optional)
5. **Enable auto-deploy** for continuous deployment

🎉 **Your RAGSPRO Dashboard is ready for production!**
