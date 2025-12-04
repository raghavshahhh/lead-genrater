# Render Environment Variables Setup

## Problem

Config file (`config/settings.json`) is not deployed to Render for security reasons.
Solution: Use environment variables instead!

## Required Environment Variables

Set these in Render Dashboard → Environment → Environment Variables:

### 1. SERPAPI_KEY (Required)
```
SERPAPI_KEY=793519f7f024954f8adaec7419aab0e07fb01449bf17f2cb89b0ffac053f860c
```

### 2. GEMINI_API_KEY (Required for AI)
```
GEMINI_API_KEY=AIzaSyCgPGrLuQrC9DeIqZvJjcnh2V1KoL8Lgyg
```

### 3. GOOGLE_SHEET_ID (Optional)
```
GOOGLE_SHEET_ID=1273CmQuy94PGHbNFVfi-4AB4XC6PkRgB1gnBti_gqjM
```

### 4. GMAIL Settings (Optional)
```
GMAIL_ADDRESS=ragsproai@gmail.com
GMAIL_APP_PASSWORD=yvyldsipoznkiyuk
```

## How to Set in Render

### Step 1: Go to Render Dashboard
1. Open: https://dashboard.render.com
2. Click on your service: "lead-generator"
3. Go to "Environment" tab

### Step 2: Add Environment Variables
Click "Add Environment Variable" and add each one:

```
Key: SERPAPI_KEY
Value: 793519f7f024954f8adaec7419aab0e07fb01449bf17f2cb89b0ffac053f860c
```

```
Key: GEMINI_API_KEY  
Value: AIzaSyCgPGrLuQrC9DeIqZvJjcnh2V1KoL8Lgyg
```

```
Key: GMAIL_ADDRESS
Value: ragsproai@gmail.com
```

```
Key: GMAIL_APP_PASSWORD
Value: yvyldsipoznkiyuk
```

### Step 3: Save and Redeploy
1. Click "Save Changes"
2. Render will automatically redeploy
3. Wait 2-3 minutes

## Benefits of Environment Variables

✅ **Secure** - No sensitive data in code
✅ **Production-ready** - Industry standard
✅ **Easy to update** - Change without code deploy
✅ **No config file needed** - Works everywhere

## How It Works

**Code checks in this order**:
1. Environment variable (Render)
2. Config file (Local development)
3. Error if neither found

**Example**:
```python
# Try environment variable first
api_key = os.getenv('SERPAPI_KEY')

# Fallback to config file
if not api_key:
    config = load_config()
    api_key = config.get('SERPAPI_KEY')
```

## Testing

After setting environment variables:
1. Go to dashboard
2. Click "Generate Premium Leads"
3. Should work without config file error!
4. Real leads will be generated

## Troubleshooting

**If still getting config error**:
1. Check environment variables are set correctly
2. Check spelling (case-sensitive!)
3. Click "Manual Deploy" to force redeploy
4. Check logs for any errors

**Common Issues**:
- Typo in variable name → Double check spelling
- Missing value → Make sure value is pasted
- Not saved → Click "Save Changes" button
- Old deployment → Wait for redeploy to finish

---

**Status**: Environment variables solution ready
**Date**: December 4, 2025
**Impact**: Works on Render without config file!
