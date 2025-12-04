# 🌐 DEPLOY ONLINE - Complete Guide

## ✅ Ise Online Karne Ke 3 Options

### Option 1: **Render.com** (Recommended - FREE)
- ✅ FREE hosting
- ✅ Easy setup
- ✅ Automatic deployments
- ✅ HTTPS included

### Option 2: **Railway.app** (Good - FREE tier)
- ✅ FREE $5/month credit
- ✅ Very easy setup
- ✅ Good performance

### Option 3: **PythonAnywhere** (Basic - FREE)
- ✅ FREE tier available
- ✅ Python-focused
- ⚠️ Limited resources

**Main Render.com recommend karta hoon - sabse easy aur reliable!**

---

## 🚀 Step-by-Step Deployment (Render.com)

### Step 1: GitHub Pe Code Upload Karo

#### A. GitHub Account Banao (agar nahi hai)
1. Go to: https://github.com
2. Sign up (free)

#### B. New Repository Banao
1. Click "New Repository"
2. Name: `lead-generation-bot`
3. Description: "Premium Lead Generation System"
4. Keep it **Private** (important - API keys hai)
5. Click "Create Repository"

#### C. Code Upload Karo

**Terminal mein:**
```bash
# 1. Git initialize karo
git init

# 2. .gitignore file banao (important!)
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
.venv/
env/

# Data files
data/*.json
data/*.csv
*.log

# Config (IMPORTANT - don't upload API keys!)
config/settings.json

# IDE
.vscode/
.idea/
.DS_Store

# Kiro
.kiro/

# Archives
docs/archive/
EOF

# 3. Files add karo
git add .

# 4. Commit karo
git commit -m "Initial commit - Premium Lead Generation System"

# 5. GitHub se connect karo
git remote add origin https://github.com/YOUR_USERNAME/lead-generation-bot.git

# 6. Push karo
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your GitHub username!**

---

### Step 2: Render.com Pe Deploy Karo

#### A. Render Account Banao
1. Go to: https://render.com
2. Sign up with GitHub (easy login)

#### B. New Web Service Banao
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select `lead-generation-bot`

#### C. Configure Settings
```
Name: lead-generation-bot
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: python dashboard_premium.py
```

#### D. Environment Variables Add Karo
Click "Environment" tab, add:
```
GEMINI_API_KEY = your-gemini-key-here
GMAIL_ADDRESS = your@gmail.com
GMAIL_APP_PASSWORD = your-16-char-password
MIN_RATING = 4.0
MIN_REVIEWS = 50
MAX_LEADS_PER_RUN = 50
```

#### E. Deploy Karo!
1. Click "Create Web Service"
2. Wait 5-10 minutes
3. Your app will be live at: `https://lead-generation-bot.onrender.com`

---

### Step 3: Files Prepare Karo (Important!)

#### A. Create `runtime.txt`
```bash
cat > runtime.txt << 'EOF'
python-3.11.0
EOF
```

#### B. Update `requirements.txt`
```bash
cat > requirements.txt << 'EOF'
flask==3.0.0
google-generativeai==0.8.3
beautifulsoup4==4.12.3
requests==2.32.5
selenium==4.15.2
webdriver-manager==4.0.1
pywhatkit==5.4
gunicorn==21.2.0
EOF
```

#### C. Create `Procfile` (for deployment)
```bash
cat > Procfile << 'EOF'
web: gunicorn dashboard_premium:app --bind 0.0.0.0:$PORT
EOF
```

#### D. Update `dashboard_premium.py` (last line)
Change:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

To:
```python
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

#### E. Create `config/settings.example.json`
```bash
mkdir -p config
cat > config/settings.example.json << 'EOF'
{
  "GEMINI_API_KEY": "get-from-environment",
  "GMAIL_ADDRESS": "get-from-environment",
  "GMAIL_APP_PASSWORD": "get-from-environment",
  "MIN_RATING": 4.0,
  "MIN_REVIEWS": 50,
  "MAX_LEADS_PER_RUN": 50,
  "GOOGLE_SHEET_ID": "",
  "GOOGLE_SERVICE_ACCOUNT_JSON": ""
}
EOF
```

#### F. Update `src/config.py` to read from environment
Add at top:
```python
import os

# Load from environment variables first
def load_config(config_path: str = "config/settings.json") -> dict[str, Any]:
    # Try environment variables first (for deployment)
    config = {
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
        "GMAIL_ADDRESS": os.getenv("GMAIL_ADDRESS"),
        "GMAIL_APP_PASSWORD": os.getenv("GMAIL_APP_PASSWORD"),
        "MIN_RATING": float(os.getenv("MIN_RATING", "4.0")),
        "MIN_REVIEWS": int(os.getenv("MIN_REVIEWS", "50")),
        "MAX_LEADS_PER_RUN": int(os.getenv("MAX_LEADS_PER_RUN", "50")),
        "GOOGLE_SHEET_ID": os.getenv("GOOGLE_SHEET_ID", ""),
        "GOOGLE_SERVICE_ACCOUNT_JSON": os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "")
    }
    
    # If no environment variables, try config file
    if not config["GEMINI_API_KEY"] and os.path.exists(config_path):
        with open(config_path, 'r') as f:
            file_config = json.load(f)
            config.update(file_config)
    
    return config
```

---

### Step 4: Push Changes to GitHub

```bash
# Add new files
git add .

# Commit
git commit -m "Add deployment files for Render"

# Push
git push origin main
```

**Render will automatically redeploy!**

---

## 🎯 Alternative: Railway.app Deployment

### Quick Steps:
1. Go to: https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub"
4. Select your repository
5. Add environment variables (same as Render)
6. Deploy!

**Railway gives you: `https://your-app.up.railway.app`**

---

## 🎯 Alternative: PythonAnywhere Deployment

### Quick Steps:
1. Go to: https://www.pythonanywhere.com
2. Sign up (free account)
3. Upload code via "Files" tab
4. Create new web app (Flask)
5. Configure WSGI file
6. Add environment variables
7. Reload web app

**PythonAnywhere gives you: `https://yourusername.pythonanywhere.com`**

---

## ⚙️ Important Configuration

### A. Update Dashboard URL
In `dashboard_premium.py`, change:
```python
print("🚀 Dashboard running at: http://localhost:5000")
```

To:
```python
print("🚀 Dashboard running at: https://your-app.onrender.com")
```

### B. CORS Settings (if needed)
Add to `dashboard_premium.py`:
```python
from flask_cors import CORS
CORS(app)
```

And add to `requirements.txt`:
```
flask-cors==4.0.0
```

### C. Security Settings
**NEVER commit:**
- `config/settings.json` (has API keys)
- `data/*.json` (has lead data)
- `.env` files

**Always use environment variables for production!**

---

## 🔒 Security Checklist

- [ ] `.gitignore` includes `config/settings.json`
- [ ] API keys in environment variables only
- [ ] Repository is **Private** on GitHub
- [ ] HTTPS enabled (automatic on Render/Railway)
- [ ] No sensitive data in code
- [ ] Environment variables set on hosting platform

---

## 📊 After Deployment

### Your App Will Be Live At:
- **Render:** `https://lead-generation-bot.onrender.com`
- **Railway:** `https://your-app.up.railway.app`
- **PythonAnywhere:** `https://yourusername.pythonanywhere.com`

### Access Dashboard:
1. Open URL in browser
2. Generate leads
3. Send messages
4. Track status

**Everything works online! 🎉**

---

## 🚨 Troubleshooting

### Problem: "Application Error"
**Solution:**
- Check logs on Render/Railway dashboard
- Verify environment variables set correctly
- Check `requirements.txt` has all dependencies

### Problem: "Port already in use"
**Solution:**
- Use `PORT` environment variable (automatic on Render/Railway)
- Update code to read from `os.environ.get('PORT')`

### Problem: "Module not found"
**Solution:**
- Add missing module to `requirements.txt`
- Redeploy

### Problem: "API key error"
**Solution:**
- Check environment variables on hosting platform
- Verify keys are correct
- No quotes around values

---

## 💰 Cost Breakdown

### Render.com (Recommended):
- **FREE tier:** 750 hours/month
- **Paid:** $7/month for always-on
- **Best for:** Production use

### Railway.app:
- **FREE:** $5 credit/month
- **Paid:** Pay as you go
- **Best for:** Testing & small projects

### PythonAnywhere:
- **FREE:** Limited resources
- **Paid:** $5/month for more resources
- **Best for:** Simple apps

**Recommendation: Start with Render FREE, upgrade if needed!**

---

## 🎉 Complete Deployment Checklist

- [ ] Code on GitHub (private repository)
- [ ] `.gitignore` configured
- [ ] `runtime.txt` created
- [ ] `Procfile` created
- [ ] `requirements.txt` updated
- [ ] Environment variables configured
- [ ] Render/Railway account created
- [ ] Web service deployed
- [ ] Environment variables added
- [ ] App tested online
- [ ] Dashboard accessible
- [ ] Lead generation working
- [ ] Messages sending

---

## 📞 Quick Commands

```bash
# 1. Prepare for deployment
git init
git add .
git commit -m "Initial commit"

# 2. Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/lead-generation-bot.git
git push -u origin main

# 3. Deploy on Render
# Go to render.com → New Web Service → Connect GitHub

# 4. Add environment variables
# On Render dashboard → Environment tab

# 5. Deploy!
# Automatic on Render

# 6. Access your app
# https://your-app.onrender.com
```

---

## ✅ Summary

**To deploy online:**
1. ✅ Upload code to GitHub (private)
2. ✅ Create Render.com account
3. ✅ Connect GitHub repository
4. ✅ Add environment variables
5. ✅ Deploy!

**Your app will be live in 10 minutes! 🚀**

**URL:** `https://your-app.onrender.com`

**Sab kuch online working! 🎉**
