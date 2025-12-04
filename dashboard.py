"""Modern Web Dashboard for Lead Generation Bot."""

from flask import Flask, render_template, jsonify, request
import sys
import os
import csv
import json
from datetime import datetime
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import load_config
from src.main_free import run_free

app = Flask(__name__)

# Global state
generation_status = {
    'running': False,
    'progress': 0,
    'message': 'Ready',
    'last_run': None,
    'total_leads': 0
}


def read_leads_from_csv():
    """Read all leads from CSV file."""
    csv_path = "data/all_leads.csv"
    if not os.path.exists(csv_path):
        return []
    
    leads = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                leads.append(row)
    except Exception as e:
        print(f"Error reading CSV: {e}")
    
    return leads


def run_generation_background():
    """Run lead generation in background with proper logging."""
    global generation_status
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        generation_status['running'] = True
        generation_status['message'] = 'Starting lead generation...'
        generation_status['progress'] = 10
        
        logger.info("🚀 Starting lead generation from dashboard")
        
        # Run the lead generation
        total_leads = run_free()
        
        generation_status['progress'] = 100
        generation_status['message'] = f'Complete! Generated {total_leads} new leads'
        generation_status['total_leads'] = total_leads
        generation_status['last_run'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        logger.info(f"✅ Lead generation complete: {total_leads} leads")
        
    except Exception as e:
        logger.error(f"❌ Lead generation error: {str(e)}", exc_info=True)
        generation_status['message'] = f'Error: {str(e)}'
        generation_status['progress'] = 0
    finally:
        generation_status['running'] = False


@app.route('/')
def index():
    """Main dashboard page - Modern RagsPro style."""
    return render_template('modern_dashboard.html')


@app.route('/api/leads')
def get_leads():
    """Get all leads."""
    leads = read_leads_from_csv()
    return jsonify({
        'success': True,
        'leads': leads,
        'total': len(leads)
    })


@app.route('/api/search')
def search_leads():
    """Search leads by keyword."""
    query = request.args.get('q', '').lower()
    leads = read_leads_from_csv()
    
    if query:
        filtered = []
        for lead in leads:
            # Search in business name, city, category
            if (query in lead.get('business_name', '').lower() or
                query in lead.get('city', '').lower() or
                query in lead.get('category', '').lower()):
                filtered.append(lead)
        leads = filtered
    
    return jsonify({
        'success': True,
        'leads': leads,
        'total': len(leads)
    })


@app.route('/api/stats')
def get_stats():
    """Get dashboard statistics."""
    leads = read_leads_from_csv()
    
    # Calculate stats
    total_leads = len(leads)
    avg_rating = sum(float(l.get('rating', 0)) for l in leads) / total_leads if total_leads > 0 else 0
    
    # Count by status
    status_counts = {}
    for lead in leads:
        status = lead.get('status', 'Unknown')
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Count by city
    city_counts = {}
    for lead in leads:
        city = lead.get('city', 'Unknown')
        city_counts[city] = city_counts.get(city, 0) + 1
    
    return jsonify({
        'success': True,
        'stats': {
            'total_leads': total_leads,
            'avg_rating': round(avg_rating, 2),
            'status_breakdown': status_counts,
            'top_cities': dict(sorted(city_counts.items(), key=lambda x: x[1], reverse=True)[:5]),
            'last_run': generation_status.get('last_run', 'Never')
        }
    })


@app.route('/api/generate', methods=['POST'])
def generate_leads():
    """Start lead generation."""
    global generation_status
    
    if generation_status['running']:
        return jsonify({
            'success': False,
            'message': 'Generation already running'
        })
    
    # Start generation in background thread
    thread = threading.Thread(target=run_generation_background)
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'success': True,
        'message': 'Lead generation started'
    })


@app.route('/api/send-outreach', methods=['POST'])
def send_outreach():
    """Send automated outreach to leads."""
    try:
        data = request.json
        lead_ids = data.get('lead_ids', [])
        send_email = data.get('send_email', True)
        send_whatsapp = data.get('send_whatsapp', False)
        
        if not lead_ids:
            return jsonify({
                'success': False,
                'message': 'No leads selected'
            })
        
        # Get leads
        all_leads = read_leads_from_csv()
        selected_leads = [all_leads[i] for i in lead_ids if i < len(all_leads)]
        
        # Start outreach in background
        thread = threading.Thread(
            target=send_outreach_background,
            args=(selected_leads, send_email, send_whatsapp)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'message': f'Outreach started for {len(selected_leads)} leads'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })


def send_outreach_background(leads, send_email, send_whatsapp):
    """Send outreach in background."""
    from src.ai_gemini import create_ai_assistant
    from src.email_sender import create_gmail_sender
    
    try:
        config = load_config()
        
        # Initialize AI
        ai = None
        if config.get('GEMINI_API_KEY'):
            ai = create_ai_assistant(config['GEMINI_API_KEY'])
        
        # Initialize email sender
        email_sender = None
        if send_email and config.get('GMAIL_ADDRESS'):
            email_sender = create_gmail_sender(
                config['GMAIL_ADDRESS'],
                config['GMAIL_APP_PASSWORD']
            )
        
        # Process each lead
        for lead in leads:
            try:
                # Generate content
                if ai:
                    email_content = ai.generate_cold_email(
                        lead['business_name'],
                        lead['category'],
                        lead['city'],
                        float(lead['rating']),
                        int(lead['reviews_count'])
                    )
                    
                    whatsapp_content = ai.generate_whatsapp_message(
                        lead['business_name'],
                        lead['category']
                    )
                else:
                    email_content = f"Hi, I noticed {lead['business_name']} has great reviews! Would love to help you get more customers online. - Raghav, RagsPro.com"
                    whatsapp_content = f"Hi! Noticed {lead['business_name']} - great business! Can we help you get more customers? - Raghav, RagsPro.com"
                
                # Send email
                if send_email and email_sender and lead.get('phone'):
                    # Note: We need email address, not phone
                    # This is a limitation - we'll log it
                    logger.info(f"Email content generated for {lead['business_name']}")
                
                # Send WhatsApp (requires pywhatkit)
                if send_whatsapp and lead.get('phone'):
                    logger.info(f"WhatsApp content generated for {lead['business_name']}")
                    # Note: Actual sending requires pywhatkit which opens browser
                    # For now, we'll save the content
                
                time.sleep(2)  # Rate limiting
                
            except Exception as e:
                logger.error(f"Error processing lead {lead['business_name']}: {e}")
        
        logger.info(f"Outreach complete for {len(leads)} leads")
        
    except Exception as e:
        logger.error(f"Error in outreach: {e}")


@app.route('/api/status')
def get_status():
    """Get generation status."""
    return jsonify({
        'success': True,
        'status': generation_status
    })


@app.route('/api/config')
def get_config():
    """Get current configuration."""
    try:
        config = load_config()
        # Hide sensitive data
        safe_config = {
            'max_leads': config.get('MAX_LEADS_PER_RUN'),
            'min_rating': config.get('MIN_RATING'),
            'min_reviews': config.get('MIN_REVIEWS'),
            'ai_enabled': bool(config.get('GEMINI_API_KEY')),
            'email_enabled': bool(config.get('GMAIL_ADDRESS'))
        }
        return jsonify({
            'success': True,
            'config': safe_config
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


if __name__ == '__main__':
    print("🚀 Starting Lead Generation Dashboard...")
    print("📊 Open browser: http://localhost:8080")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=8080)
