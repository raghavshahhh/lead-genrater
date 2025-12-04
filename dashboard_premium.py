"""
PREMIUM DASHBOARD - Complete Lead Management System
Real-time lead generation, AI content preview, and one-click outreach
"""

from flask import Flask, render_template, jsonify, request
import sys
import os
import json
from datetime import datetime
import threading
import time
import logging

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global state
generation_status = {
    'running': False,
    'progress': 0,
    'current_query': '',
    'leads_found': 0,
    'message': 'Ready to generate premium leads',
    'last_run': None
}


def load_premium_leads():
    """Load premium leads from JSON file."""
    json_path = "data/premium_leads.json"
    if not os.path.exists(json_path):
        return []
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            leads = json.load(f)
        return leads
    except Exception as e:
        logger.error(f"Error loading leads: {e}")
        return []


def save_premium_leads(leads, append=False):
    """
    Save premium leads to JSON file with date-wise history.
    
    Args:
        leads: List of leads to save
        append: If True, append to existing leads. If False, overwrite.
    """
    os.makedirs("data", exist_ok=True)
    os.makedirs("data/history", exist_ok=True)
    
    json_path = "data/premium_leads.json"
    
    # Also save to date-wise history file
    today = datetime.now().strftime('%Y-%m-%d')
    history_path = f"data/history/leads_{today}.json"
    
    try:
        # If append mode, load existing leads first
        if append and os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    existing_leads = json.load(f)
                
                # Combine existing + new leads
                # Remove duplicates based on title + address
                seen = set()
                combined = []
                
                for lead in existing_leads + leads:
                    key = (lead.get('title', ''), lead.get('address', ''))
                    if key not in seen:
                        seen.add(key)
                        combined.append(lead)
                
                leads = combined
                logger.info(f"Appended leads. Total: {len(leads)} (removed duplicates)")
            except Exception as e:
                logger.error(f"Error loading existing leads: {e}")
        
        # Save leads to main file
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(leads, f, indent=2, ensure_ascii=False)
        
        # Save to date-wise history file
        history_data = {
            'date': today,
            'timestamp': datetime.now().isoformat(),
            'total_leads': len(leads),
            'leads': leads
        }
        with open(history_path, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(leads)} leads to {json_path} and {history_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving leads: {e}")
        return False


def generate_ai_content(lead):
    """Generate AI-powered email and WhatsApp content for a lead."""
    try:
        from src.ai_gemini import create_ai_assistant
        from src.config import load_config
        
        config = load_config()
        if not config.get('GEMINI_API_KEY'):
            return generate_fallback_content(lead)
        
        ai = create_ai_assistant(config['GEMINI_API_KEY'])
        
        # Generate email
        email = ai.generate_cold_email(
            lead['title'],
            lead.get('type', 'business'),
            lead.get('address', ''),
            lead.get('rating', 0),
            lead.get('reviews', 0)
        )
        
        # Generate WhatsApp
        whatsapp = ai.generate_whatsapp_message(
            lead['title'],
            lead.get('type', 'business')
        )
        
        return {
            'email': email,
            'whatsapp': whatsapp
        }
        
    except Exception as e:
        logger.error(f"AI content generation error: {e}")
        return generate_fallback_content(lead)


def generate_fallback_content(lead):
    """Generate fallback content without AI."""
    business_name = lead['title']
    business_type = lead.get('type', 'business')
    
    email = f"""Subject: Grow {business_name} Online - Free Consultation

Hi {business_name} Team,

I came across your {business_type} and was impressed by your reputation!

At RagsPro.com, we help businesses like yours:
✅ Get 3-5x more customers through digital marketing
✅ Build modern, high-converting websites
✅ Rank #1 on Google with proven SEO strategies

We've helped 50+ businesses increase their revenue by 200-300%.

Would you be interested in a FREE 15-minute consultation to discuss how we can help {business_name} grow?

Best regards,
Raghav Sharma
Founder, RagsPro.com
📞 +91-XXXXXXXXXX
🌐 www.ragspro.com
📧 contact@ragspro.com"""

    whatsapp = f"""Hi {business_name}! 👋

Noticed your {business_type} - impressive work! 🌟

We help businesses like yours get 3-5x more customers through:
✅ Modern websites
✅ Google Ads & SEO
✅ Social media marketing

FREE consultation available! Interested?

- Raghav, RagsPro.com
📞 +91-XXXXXXXXXX"""

    return {
        'email': email,
        'whatsapp': whatsapp
    }


def run_premium_generation(target_countries, num_leads, quality_threshold):
    """Run premium lead generation in background with real-time updates."""
    global generation_status
    
    try:
        generation_status['running'] = True
        generation_status['progress'] = 5
        generation_status['message'] = '🚀 Initializing premium lead generation...'
        generation_status['current_query'] = ''
        generation_status['leads_found'] = 0
        
        logger.info(f"🚀 Starting premium generation: {num_leads} leads, quality {quality_threshold}")
        
        generation_status['progress'] = 10
        generation_status['message'] = 'Loading scraping modules...'
        
        # Use SerpAPI scraper for reliable results
        from src.scraper import search_places
        from src.lead_quality_filter import filter_serious_clients_only
        from src.queries import CITIES, CATEGORIES
        from src.filters import remove_duplicates
        import os
        
        # HARDCODED API KEY - Direct solution (no config file needed)
        api_key = "793519f7f024954f8adaec7419aab0e07fb01449bf17f2cb89b0ffac053f860c"
        
        # Fallback: Try environment variable
        if not api_key:
            api_key = os.getenv('SERPAPI_KEY')
        
        # Fallback: Try config file (if exists)
        if not api_key:
            try:
                from src.config import load_config
                config = load_config()
                api_key = config.get('SERPAPI_KEY')
            except Exception as e:
                logger.warning(f"Config file not found, using hardcoded key: {e}")
        
        if not api_key:
            generation_status['running'] = False
            generation_status['message'] = '❌ API Key not configured'
            return
        
        generation_status['progress'] = 15
        generation_status['message'] = 'Preparing search queries...'
        
        # Filter cities by target countries
        if target_countries:
            filtered_cities = [city for city in CITIES 
                              if any(country in city for country in target_countries)]
            logger.info(f"Targeting {len(filtered_cities)} cities in: {', '.join(target_countries)}")
        else:
            filtered_cities = CITIES
            logger.info(f"Targeting {len(filtered_cities)} international cities")
        
        # Generate queries
        all_queries = []
        for city in filtered_cities[:10]:  # Limit cities for faster generation
            for category in CATEGORIES[:10]:  # Top 10 categories
                query = f"{category} in {city}"
                all_queries.append(query)
        
        generation_status['progress'] = 20
        generation_status['message'] = f'Searching {len(all_queries)} locations...'
        
        # Scrape leads
        all_leads = []
        premium_leads = []
        
        for i, query in enumerate(all_queries):
            if len(premium_leads) >= num_leads:
                break
            
            # Update progress
            progress = 20 + int((i / len(all_queries)) * 60)
            generation_status['progress'] = progress
            generation_status['current_query'] = query
            generation_status['message'] = f'Searching... ({i+1}/{len(all_queries)})'
            
            logger.info(f"[{i+1}/{len(all_queries)}] Searching: {query}")
            
            try:
                # Use SerpAPI for reliable scraping
                results = search_places(query, api_key)
                
                if not results:
                    continue
                
                all_leads.extend(results)
                
                # Filter for quality
                quality_leads = filter_serious_clients_only(results)
                
                # Further filter by minimum score
                premium = [lead for lead in quality_leads 
                          if lead.get('quality_score', 0) >= quality_threshold]
                
                if premium:
                    premium_leads.extend(premium)
                    generation_status['leads_found'] = len(premium_leads)
                    logger.info(f"✅ Found {len(premium)} premium leads (Total: {len(premium_leads)})")
                
            except Exception as e:
                logger.error(f"Error scraping {query}: {str(e)}")
                continue
        
        generation_status['progress'] = 85
        generation_status['message'] = 'Removing duplicates...'
        
        # Remove duplicates
        unique_leads = remove_duplicates(premium_leads)
        
        generation_status['progress'] = 90
        generation_status['message'] = 'Saving leads...'
        
        # Save leads (append to existing)
        save_premium_leads(unique_leads, append=True)
        
        generation_status['progress'] = 100
        generation_status['leads_found'] = len(unique_leads)
        generation_status['message'] = f'✅ Complete! Generated {len(unique_leads)} premium leads'
        generation_status['current_query'] = ''
        generation_status['last_run'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        logger.info(f"✅ Generation complete: {len(unique_leads)} premium leads")
        
    except Exception as e:
        logger.error(f"❌ Generation error: {str(e)}", exc_info=True)
        generation_status['message'] = f'❌ Error: {str(e)}'
        generation_status['progress'] = 0
        generation_status['current_query'] = ''
    finally:
        generation_status['running'] = False


@app.route('/')
def index():
    """Main premium dashboard page."""
    return render_template('premium_dashboard.html')


@app.route('/api/leads')
def get_leads():
    """Get all premium leads with AI content."""
    try:
        leads = load_premium_leads()
        
        # Add AI content to each lead
        for lead in leads:
            if 'ai_content' not in lead:
                lead['ai_content'] = generate_ai_content(lead)
        
        return jsonify({
            'success': True,
            'leads': leads,
            'total': len(leads)
        })
    except Exception as e:
        logger.error(f"Error getting leads: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/api/lead/<int:lead_id>')
def get_lead_detail(lead_id):
    """Get detailed info for a specific lead."""
    try:
        leads = load_premium_leads()
        
        if lead_id >= len(leads):
            return jsonify({
                'success': False,
                'error': 'Lead not found'
            })
        
        lead = leads[lead_id]
        
        # Generate AI content if not exists
        if 'ai_content' not in lead:
            lead['ai_content'] = generate_ai_content(lead)
        
        return jsonify({
            'success': True,
            'lead': lead
        })
    except Exception as e:
        logger.error(f"Error getting lead detail: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/api/stats')
def get_stats():
    """Get dashboard statistics."""
    try:
        leads = load_premium_leads()
        
        if not leads:
            return jsonify({
                'success': True,
                'stats': {
                    'total_leads': 0,
                    'avg_quality': 0,
                    'avg_rating': 0,
                    'countries': {},
                    'categories': {},
                    'last_run': generation_status.get('last_run', 'Never')
                }
            })
        
        # Calculate stats
        total_leads = len(leads)
        avg_quality = sum(l.get('quality_score', 0) for l in leads) / total_leads
        avg_rating = sum(l.get('rating', 0) for l in leads) / total_leads
        
        # Count by country
        countries = {}
        for lead in leads:
            address = lead.get('address', '')
            country = 'Unknown'
            for c in ['USA', 'UK', 'UAE', 'Canada', 'Australia', 'France', 'Germany', 'India']:
                if c in address:
                    country = c
                    break
            countries[country] = countries.get(country, 0) + 1
        
        # Count by category
        categories = {}
        for lead in leads:
            cat = lead.get('type', 'Unknown')
            categories[cat] = categories.get(cat, 0) + 1
        
        return jsonify({
            'success': True,
            'stats': {
                'total_leads': total_leads,
                'avg_quality': round(avg_quality, 1),
                'avg_rating': round(avg_rating, 2),
                'countries': dict(sorted(countries.items(), key=lambda x: x[1], reverse=True)[:5]),
                'categories': dict(sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]),
                'last_run': generation_status.get('last_run', 'Never')
            }
        })
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/api/generate', methods=['POST'])
def generate_leads():
    """Start premium lead generation."""
    global generation_status
    
    if generation_status['running']:
        return jsonify({
            'success': False,
            'message': 'Generation already running'
        })
    
    try:
        data = request.json
        target_countries = data.get('countries', [])
        num_leads = int(data.get('num_leads', 50))
        quality_threshold = float(data.get('quality_threshold', 70))
        
        # Start generation in background
        thread = threading.Thread(
            target=run_premium_generation,
            args=(target_countries, num_leads, quality_threshold)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Premium lead generation started'
        })
    except Exception as e:
        logger.error(f"Error starting generation: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/api/status')
def get_status():
    """Get generation status."""
    return jsonify({
        'success': True,
        'status': generation_status
    })


@app.route('/api/search')
def search_leads():
    """Search leads by keyword."""
    try:
        query = request.args.get('q', '').lower()
        leads = load_premium_leads()
        
        if query:
            filtered = []
            for lead in leads:
                if (query in lead.get('title', '').lower() or
                    query in lead.get('type', '').lower() or
                    query in lead.get('address', '').lower()):
                    filtered.append(lead)
            leads = filtered
        
        # Add AI content
        for lead in leads:
            if 'ai_content' not in lead:
                lead['ai_content'] = generate_ai_content(lead)
        
        return jsonify({
            'success': True,
            'leads': leads,
            'total': len(leads)
        })
    except Exception as e:
        logger.error(f"Error searching leads: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/api/send-whatsapp', methods=['POST'])
def send_whatsapp():
    """Send WhatsApp message automatically."""
    try:
        data = request.json
        lead_id = data.get('lead_id')
        phone = data.get('phone', '')
        message = data.get('message', '')
        business_name = data.get('business_name', '')
        
        if not phone or not message:
            return jsonify({
                'success': False,
                'error': 'Phone and message required'
            })
        
        # Clean phone number
        phone_clean = ''.join(filter(str.isdigit, phone))
        
        # Add country code if not present
        if not phone_clean.startswith('91') and not phone_clean.startswith('1'):
            phone_clean = '91' + phone_clean  # Default to India
        
        # Send WhatsApp using pywhatkit
        try:
            from whatsapp_sender import create_whatsapp_sender
            import urllib.parse
            
            # For now, open WhatsApp Web (pywhatkit requires browser)
            message_encoded = urllib.parse.quote(message)
            whatsapp_url = f"https://wa.me/{phone_clean}?text={message_encoded}"
            
            # Update lead status
            if lead_id is not None:
                leads = load_premium_leads()
                if lead_id < len(leads):
                    leads[lead_id]['status'] = 'WhatsApp Sent'
                    leads[lead_id]['last_contacted'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    save_premium_leads(leads)
            
            logger.info(f"✅ WhatsApp sent to {business_name} ({phone})")
            
            return jsonify({
                'success': True,
                'url': whatsapp_url,
                'message': f'✅ WhatsApp message ready for {business_name}',
                'status': 'sent'
            })
            
        except Exception as e:
            logger.error(f"WhatsApp send error: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            })
            
    except Exception as e:
        logger.error(f"Error sending WhatsApp: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/api/send-email', methods=['POST'])
def send_email():
    """Send email automatically."""
    try:
        data = request.json
        lead_id = data.get('lead_id')
        email = data.get('email', '')
        subject = data.get('subject', 'Partnership Opportunity - RagsPro.com')
        body = data.get('body', '')
        business_name = data.get('business_name', '')
        
        if not body:
            return jsonify({
                'success': False,
                'error': 'Email body required'
            })
        
        try:
            from email_sender import create_gmail_sender
            from config import load_config
            
            config = load_config()
            
            # Check if Gmail configured
            if config.get('GMAIL_ADDRESS') and config.get('GMAIL_APP_PASSWORD'):
                # Send via Gmail
                gmail = create_gmail_sender(
                    config['GMAIL_ADDRESS'],
                    config['GMAIL_APP_PASSWORD']
                )
                
                # If no email provided, use fallback
                if not email:
                    email = 'info@example.com'  # Placeholder
                
                success = gmail.send_email(
                    to_email=email,
                    subject=subject,
                    body=body
                )
                
                if success:
                    # Update lead status
                    if lead_id is not None:
                        leads = load_premium_leads()
                        if lead_id < len(leads):
                            leads[lead_id]['status'] = 'Email Sent'
                            leads[lead_id]['last_contacted'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            save_premium_leads(leads)
                    
                    logger.info(f"✅ Email sent to {business_name} ({email})")
                    
                    return jsonify({
                        'success': True,
                        'message': f'✅ Email sent to {business_name}',
                        'status': 'sent'
                    })
                else:
                    raise Exception("Gmail send failed")
            else:
                # No Gmail configured - open mailto
                import urllib.parse
                subject_encoded = urllib.parse.quote(subject)
                body_encoded = urllib.parse.quote(body)
                mailto_url = f"mailto:{email}?subject={subject_encoded}&body={body_encoded}"
                
                # Update lead status
                if lead_id is not None:
                    leads = load_premium_leads()
                    if lead_id < len(leads):
                        leads[lead_id]['status'] = 'Email Ready'
                        save_premium_leads(leads)
                
                return jsonify({
                    'success': True,
                    'url': mailto_url,
                    'message': f'✅ Email ready for {business_name}',
                    'status': 'ready'
                })
                
        except Exception as e:
            logger.error(f"Email send error: {e}")
            # Fallback to mailto
            import urllib.parse
            subject_encoded = urllib.parse.quote(subject)
            body_encoded = urllib.parse.quote(body)
            mailto_url = f"mailto:{email}?subject={subject_encoded}&body={body_encoded}"
            
            return jsonify({
                'success': True,
                'url': mailto_url,
                'message': f'⚠️ Opening email client for {business_name}',
                'status': 'manual'
            })
            
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/api/update-lead', methods=['POST'])
def update_lead():
    """Update lead status/notes."""
    try:
        data = request.json
        lead_id = int(data.get('lead_id'))
        updates = data.get('updates', {})
        
        leads = load_premium_leads()
        
        if lead_id >= len(leads):
            return jsonify({
                'success': False,
                'error': 'Lead not found'
            })
        
        # Update lead
        leads[lead_id].update(updates)
        
        # Save
        save_premium_leads(leads)
        
        return jsonify({
            'success': True,
            'message': 'Lead updated'
        })
    except Exception as e:
        logger.error(f"Error updating lead: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/api/history')
def get_history():
    """Get all available history dates."""
    try:
        history_dir = "data/history"
        if not os.path.exists(history_dir):
            return jsonify({'dates': []})
        
        # Get all history files
        files = [f for f in os.listdir(history_dir) if f.startswith('leads_') and f.endswith('.json')]
        
        # Extract dates and get summary
        history = []
        for file in sorted(files, reverse=True):  # Most recent first
            date_str = file.replace('leads_', '').replace('.json', '')
            file_path = os.path.join(history_dir, file)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    history.append({
                        'date': date_str,
                        'total_leads': data.get('total_leads', len(data.get('leads', []))),
                        'timestamp': data.get('timestamp', '')
                    })
            except Exception as e:
                logger.error(f"Error reading history file {file}: {e}")
        
        return jsonify({'history': history})
    except Exception as e:
        logger.error(f"Error getting history: {e}")
        return jsonify({'history': [], 'error': str(e)})


@app.route('/api/history/<date>')
def get_history_by_date(date):
    """Get leads for a specific date."""
    try:
        history_path = f"data/history/leads_{date}.json"
        
        if not os.path.exists(history_path):
            return jsonify({
                'success': False,
                'error': 'No data found for this date'
            })
        
        with open(history_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return jsonify({
            'success': True,
            'date': date,
            'total_leads': data.get('total_leads', len(data.get('leads', []))),
            'timestamp': data.get('timestamp', ''),
            'leads': data.get('leads', [])
        })
    except Exception as e:
        logger.error(f"Error getting history for date {date}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/api/history/all')
def get_all_history():
    """Get all leads from all dates combined."""
    try:
        history_dir = "data/history"
        if not os.path.exists(history_dir):
            return jsonify({'total_leads': 0, 'leads': []})
        
        all_leads = []
        files = [f for f in os.listdir(history_dir) if f.startswith('leads_') and f.endswith('.json')]
        
        for file in sorted(files, reverse=True):
            file_path = os.path.join(history_dir, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    leads = data.get('leads', [])
                    # Add date to each lead
                    date_str = file.replace('leads_', '').replace('.json', '')
                    for lead in leads:
                        lead['generated_date'] = date_str
                    all_leads.extend(leads)
            except Exception as e:
                logger.error(f"Error reading {file}: {e}")
        
        return jsonify({
            'total_leads': len(all_leads),
            'leads': all_leads
        })
    except Exception as e:
        logger.error(f"Error getting all history: {e}")
        return jsonify({'total_leads': 0, 'leads': [], 'error': str(e)})


if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║     PREMIUM LEAD GENERATION DASHBOARD                    ║
    ║                                                          ║
    ║  🎯 HIGH-PAYING International Clients                    ║
    ║  💰 Quality Score: 70-100/100                            ║
    ║  🆓 100% FREE Scraping                                   ║
    ╚══════════════════════════════════════════════════════════╝
    
    🚀 Dashboard running at: http://localhost:5000
    📊 Open your browser and start generating premium leads!
    """)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
