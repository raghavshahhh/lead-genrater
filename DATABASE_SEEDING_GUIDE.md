# 🌱 Database Seeding Guide - Pre-populate with Real Leads

## Overview

This script pre-populates your database with **REAL verified leads** from SerpAPI.

**No dummy data. No demo data. 100% real businesses.**

## What Gets Seeded

### Cities (50 total):
- **USA:** New York, Los Angeles, Chicago, Houston, Miami
- **UK:** London, Manchester, Birmingham, Edinburgh, Liverpool
- **UAE:** Dubai, Abu Dhabi, Sharjah, Ajman, Ras Al Khaimah
- **Canada:** Toronto, Vancouver, Montreal, Calgary, Ottawa
- **Australia:** Sydney, Melbourne, Brisbane, Perth, Adelaide
- **India:** Mumbai, Delhi, Bangalore, Hyderabad, Chennai
- **Singapore:** Singapore
- **Germany:** Berlin, Munich, Frankfurt, Hamburg, Cologne
- **France:** Paris, Lyon, Marseille, Nice, Toulouse
- **Netherlands:** Amsterdam, Rotterdam, The Hague, Utrecht
- **Saudi Arabia:** Riyadh, Jeddah, Mecca, Medina

### Business Categories (20 total):
1. Dental clinic
2. Law firm
3. Accounting firm
4. Real estate agency
5. Software company
6. Consulting firm
7. Medical clinic
8. Cosmetic surgery
9. Investment firm
10. Architecture firm
11. Restaurant
12. Hotel
13. Cafe
14. Gym
15. Spa
16. Marketing agency
17. Web design agency
18. Photography studio
19. Event planning
20. Interior design

### Expected Results:
- **Total queries:** 50 cities × 20 categories = 1,000 queries
- **Expected leads:** ~15,000-20,000 verified leads
- **Time required:** ~2-3 hours
- **SerpAPI cost:** ~$50-100 (depending on your plan)

## Prerequisites

1. **SerpAPI Key:**
   - Get from: https://serpapi.com
   - Set in `src/config.py`:
     ```python
     SERPAPI_KEY = 'your-key-here'
     ```

2. **Python Environment:**
   ```bash
   source .venv/bin/activate  # or activate your venv
   ```

3. **Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

### Step 1: Check Configuration
```bash
# Verify SerpAPI key is set
python3 -c "from src.config import load_config; print('API Key:', load_config().get('SERPAPI_KEY')[:10] + '...')"
```

### Step 2: Run Seeding Script
```bash
python3 seed_database.py
```

### Step 3: Confirm
```
⚠️  This will use SerpAPI quota. Continue? (yes/no): yes
```

### Step 4: Wait
The script will:
- Search 1,000 queries (50 cities × 20 categories)
- Filter for quality (70+ score)
- Remove duplicates
- Save to database

**Progress will be shown:**
```
[1/1000] 🔍 Searching: dental clinic in New York, USA
   ✅ Found 18 quality leads (Total: 18)
[2/1000] 🔍 Searching: law firm in New York, USA
   ✅ Found 20 quality leads (Total: 38)
...
```

## Output Files

### 1. Main Database
```
data/premium_leads.json
```
Contains all unique verified leads.

### 2. History
```
data/history/leads_2025-12-12.json
```
Timestamped snapshot with metadata.

### 3. Backup
```
data/backups/seed_backup_20251212_190000.json
```
Safety backup of seeded data.

## Statistics

After seeding, you'll see:

```
📈 Database Statistics:

   By Country:
      USA: 3,245 leads
      UK: 2,891 leads
      UAE: 2,567 leads
      ...

   By Category (Top 10):
      dental clinic: 892 leads
      law firm: 845 leads
      restaurant: 823 leads
      ...

   By Quality Score:
      90-100: 4,523 leads
      80-89: 8,912 leads
      70-79: 5,234 leads

✅ Database seeding complete!
   Total verified leads: 18,669
   Average quality score: 84.2/100
```

## Verification

### Check Database
```bash
# Count leads
python3 -c "import json; data = json.load(open('data/premium_leads.json')); print(f'Total leads: {len(data)}')"

# Show first lead
python3 -c "import json; data = json.load(open('data/premium_leads.json')); print(json.dumps(data[0], indent=2))"
```

### Start Dashboard
```bash
python3 dashboard_ragspro.py
```

Open: http://localhost:5002

You should see all seeded leads!

## Customization

### Add More Cities
Edit `seed_database.py`:
```python
SEED_CITIES = [
    "New York, USA",
    "Your City, Country",  # Add here
    ...
]
```

### Add More Categories
```python
SEED_CATEGORIES = [
    "dental clinic",
    "your category",  # Add here
    ...
]
```

### Change Quality Threshold
```python
# Line 150 - change 70 to your threshold
premium = [lead for lead in quality_leads if lead.get('quality_score', 0) >= 70]
```

## Troubleshooting

### Problem: "SERPAPI_KEY not found"
**Solution:**
```bash
# Set in src/config.py
SERPAPI_KEY = 'your-actual-key-here'
```

### Problem: "No results found" for many queries
**Possible causes:**
- SerpAPI quota exhausted
- API key invalid
- Network issues

**Solution:**
1. Check API key
2. Check SerpAPI dashboard for quota
3. Wait and retry

### Problem: Script is slow
**Normal behavior:**
- 2 seconds delay between queries (rate limiting)
- 1,000 queries = ~33 minutes minimum
- Plus API response time

**To speed up:**
- Reduce `time.sleep(2)` to `time.sleep(1)` (risky - may hit rate limits)
- Reduce number of cities/categories

### Problem: Duplicate leads
**Solution:**
Script automatically removes duplicates based on:
- Business name
- Address

## Cost Estimation

### SerpAPI Pricing:
- Free plan: 100 searches/month
- Paid plans: $50/month for 5,000 searches

### For Full Seeding:
- Queries: 1,000
- Cost: ~$10-20 (depending on plan)

### Recommendation:
Start with fewer cities/categories to test:
```python
# Test with 5 cities × 5 categories = 25 queries
SEED_CITIES = SEED_CITIES[:5]  # First 5 cities
SEED_CATEGORIES = SEED_CATEGORIES[:5]  # First 5 categories
```

## Production Deployment

### Before Deploying:
1. Seed database locally
2. Verify data quality
3. Commit `data/premium_leads.json` to Git (if small)
4. Or upload to cloud storage

### On Render/Production:
```bash
# Option 1: Include in Git
git add data/premium_leads.json
git commit -m "Add seeded database"
git push

# Option 2: Run seeding on production
# (Not recommended - uses production API quota)
python3 seed_database.py
```

## Maintenance

### Re-seed Periodically:
```bash
# Backup old data
cp data/premium_leads.json data/backups/old_leads.json

# Run seeding again
python3 seed_database.py
```

### Merge with Existing Data:
```python
# In seed_database.py, change line 180:
# Instead of overwriting, append:
existing = json.load(open('data/premium_leads.json'))
all_leads = existing + unique_leads
# Then remove duplicates and save
```

## Success Criteria

✅ Script completes without errors  
✅ 15,000+ leads in database  
✅ Average quality score > 80  
✅ All cities represented  
✅ All categories represented  
✅ Dashboard shows all leads  
✅ Search works for all cities/categories  

**Database is now production-ready with real verified leads!** 🚀
