"""FREE AI integration using Google Gemini for pitch generation."""

import logging
import google.generativeai as genai

logger = logging.getLogger(__name__)


class GeminiAI:
    """FREE AI assistant using Google Gemini."""
    
    def __init__(self, api_key: str):
        """Initialize Gemini AI with API key."""
        genai.configure(api_key=api_key)
        # Use gemini-1.5-flash for latest model
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        logger.info("Gemini AI initialized (FREE) - using gemini-1.5-flash")
    
    def generate_cold_email(self, business_name: str, business_type: str, 
                           city: str, rating: float, reviews: int, owner_name: str = None) -> str:
        """
        Generate personalized cold email using professional template.
        
        Args:
            business_name: Name of the business
            business_type: Type/category of business
            city: City location
            rating: Google rating
            reviews: Number of reviews
            owner_name: Owner name (optional, defaults to "Team")
        
        Returns:
            Personalized email content
        """
        # Use owner name or default
        owner = owner_name if owner_name else f"{business_name} Team"
        
        prompt = f"""You are writing on behalf of Ragspro.com - a premium software development agency.

Generate a professional, SHORT cold email (under 100 words) for this prospect:

Business: {business_name}
Type: {business_type}
Location: {city}
Rating: {rating}★ ({reviews} reviews)

RAGSPRO VALUE PROPOSITION:
- Fast MVP delivery (2-4 weeks)
- Modern tech stack (React, Node.js, Python, AWS)
- Transparent pricing ($5k-$50k projects)
- Direct developer communication
- Proven track record: LawAI, Glow, HimShakti
- 200+ projects delivered, 50+ happy clients

EMAIL STRUCTURE (MUST FOLLOW):

Line 1: Personalized observation about their business
Example: "Noticed {business_name} is growing fast - congrats on {rating}★ rating!"

Line 2: Identify specific tech problem they likely have
Examples based on business type:
- SaaS/Tech: "Many companies at your stage struggle with shipping features fast while maintaining quality"
- E-commerce: "Most e-commerce brands need better checkout experience and mobile optimization"
- Fintech: "Fintech companies often need help with compliance, security, and scalability"
- Startup: "Startups need to validate ideas quickly with MVPs before full builds"

Line 3: How Ragspro solves it (brief, specific)
Example: "We've helped 50+ startups ship MVPs in 2-4 weeks using modern tech"

Line 4: Social proof (mention specific projects)
Example: "Recent work: LawAI (legal tech), Glow (AI photo editor), HimShakti (e-commerce)"

Line 5: Easy CTA (15-min call)
Example: "15-min call to explore fit? [Calendly link]"

Signature:
Raghav Shah
Founder, Ragspro.com - Software Development Agency
📞 +918700048490
📧 ragsproai@gmail.com
🌐 ragspro.com

Connect:
💼 LinkedIn: linkedin.com/in/raghavshahhh
💻 GitHub: github.com/raghavshahhhh

CRITICAL RULES:
1. Keep it under 100 words total
2. Sound like expert consultant, not salesperson
3. Be specific about tech/development (not generic marketing)
4. Mention actual projects (LawAI, Glow, HimShakti)
5. Focus on speed + quality + proven results
6. Professional but friendly tone
7. No fluff or buzzwords

Business Details:
- Name: {business_name}
- Type: {business_type}
- Location: {city}
- Rating: {rating}★ ({reviews} reviews)

YOUR AGENCY - RagsPro.com (Based in Delhi, India):
Services We Offer:
• Mobile Apps (iOS/Android) - Custom mobile applications
• Web Apps - Full-stack SaaS and web applications  
• Landing Pages - High-converting professional pages
• UX/UI Design - Modern, user-friendly interfaces
• Brand Design - Complete branding solutions
• 3D Design - Product visualization and modeling
• SEO & Digital Marketing - Google Ads, Social Media
• E-commerce Solutions - Online stores with payment integration
• AI Integration - Smart features for modern businesses
• Data Security - Enterprise-grade protection

Track Record:
- 200+ successful projects delivered
- 50+ happy clients with 5★ ratings
- Built successful SaaS: LawAI, Glow, HimShakti
- Average client revenue increase: 3-5x
- Portfolio: ragspro.com
- Contact: +918700048490 | raghav@ragspro.com

CRITICAL RULES - Professional Business Analysis Approach:

1. COMPLIMENT FIRST: Start with genuine praise about their {rating}★ rating and {reviews} reviews

2. IDENTIFY PROBLEMS (Choose 2-3 based on business type):
   Common Issues to Mention:
   - "I noticed you don't have a website" or "Your website looks outdated"
   - "No online ordering system - losing customers to competitors"
   - "Not showing up on Google searches - missing SEO"
   - "No mobile app - customers prefer apps for convenience"
   - "Social media presence is weak - not reaching younger audience"
   - "No online booking system - customers going elsewhere"
   - "Website not mobile-friendly - 70% customers use phones"
   - "Competitors have better online presence"

3. SHOW EXPERTISE: Analyze their specific business type professionally:
   - Restaurants/Cafes → "Need mobile app for orders + modern website + online menu"
   - Retail/Shops → "Need e-commerce store + payment gateway + inventory system"
   - Services → "Need professional website + SEO + Google My Business optimization"
   - Healthcare → "Need appointment booking system + patient portal + telemedicine"
   - Education → "Need learning management system + online classes + student portal"
   - Salons/Spas → "Need online booking + customer management + loyalty program"

4. PROVIDE DATA: "Businesses like yours with proper digital presence see 3-5x revenue increase"

5. MENTION REAL PROJECTS: "We built LawAI (legal tech), Glow (AI photo editor), HimShakti (e-commerce) - check ragspro.com"

6. OFFER SOLUTION: Specific RagsPro services that solve their problems

7. CREATE URGENCY: "Your competitors are already ahead - don't lose more customers"

8. FREE VALUE: "FREE website audit + business analysis + project roadmap"

9. SOCIAL PROOF: "200+ projects delivered, 50+ happy clients, 5★ ratings"

10. PROFESSIONAL TONE: Sound like expert consultant, not salesperson

11. CALL-TO-ACTION: "Reply 'YES' for FREE consultation or WhatsApp +918700048490"

12. Keep it 150-180 words (detailed but concise)

13. Use Indian English naturally, professional but friendly

Write ONLY the email body (no subject line):"""

        try:
            response = self.model.generate_content(prompt)
            email = response.text.strip()
            logger.info(f"Generated email for {business_name}")
            return email
        except Exception as e:
            logger.error(f"Gemini AI error: {str(e)}")
            return self._fallback_email(business_name, business_type, rating, reviews)
    
    def generate_whatsapp_message(self, business_name: str, business_type: str) -> str:
        """
        Generate WhatsApp intro message using Gemini AI.
        
        Args:
            business_name: Name of the business
            business_type: Type/category of business
        
        Returns:
            WhatsApp message text
        """
        prompt = f"""You are Raghav Shah from Ragspro.com - premium software development agency. Write a SHORT WhatsApp message (80-90 words) that gets response.

Business: {business_name} ({business_type})

RAGSPRO - Software Development Agency:
Core Services: MVP Development, SaaS Products, Mobile Apps, E-commerce Platforms
Unique Value: Ship MVPs in 2-4 weeks, Modern tech stack, Transparent pricing
Real Projects: LawAI (legal tech), Glow (AI photo editor), HimShakti (e-commerce)
Track Record: 200+ projects, 50+ clients, 5★ ratings
Portfolio: ragspro.com
Contact: +918700048490 | raghav@ragspro.com

MESSAGE STRUCTURE - Professional WhatsApp:

1. OPENER: "Hey! 🚀 Raghav from RagsPro.com (Delhi)"

2. COMPLIMENT + PROBLEM: "Saw {business_name} - {rating}★ rating! But noticed [specific problem]"
   Problems to mention:
   - "no website/app"
   - "outdated online presence"
   - "competitors ahead online"
   - "missing online orders/bookings"

3. SHOW EXPERTISE: Mention what they NEED based on business type:
   - Restaurants → "Mobile app for orders + website"
   - Retail → "E-commerce store + online payments"
   - Services → "Professional website + SEO"
   - Healthcare → "Booking system + patient portal"

4. CREDIBILITY: "Built LawAI, Glow, HimShakti - 200+ projects 💻"

5. URGENCY: "Competitors already using our solutions"

6. VALUE: "FREE business analysis + project roadmap ✅"

7. EMOJIS: Use 3-4 strategically: 🚀 💰 ✅ 🎯 📱 💻 🌟

8. LENGTH: 80-90 words (detailed but WhatsApp-friendly)

9. CALL-TO-ACTION: "Interested? Reply YES or call +918700048490 📱"

10. TONE: Professional but friendly, like expert consultant helping friend

Examples of GOOD style:
- "Hey! 🚀 Raghav from RagsPro.com (Delhi)"
- "Saw [business name] - great ratings! 🌟"
- "We build mobile apps, websites, SaaS for businesses like yours"
- "Built LawAI, Glow, HimShakti - check ragspro.com 💻"
- "Want [specific service]? FREE consultation! ✅"
- "Limited slots - reply YES or call +918700048490 📱"

Write the message:"""

        try:
            response = self.model.generate_content(prompt)
            message = response.text.strip()
            logger.info(f"Generated WhatsApp message for {business_name}")
            return message
        except Exception as e:
            logger.error(f"Gemini AI error: {str(e)}")
            return self._fallback_whatsapp(business_name, business_type)
    
    def analyze_business(self, business_name: str, business_type: str, 
                        rating: float, reviews: int, address: str) -> str:
        """
        Analyze business and suggest pitch angle using Gemini AI.
        
        Args:
            business_name: Name of the business
            business_type: Type/category of business
            rating: Google rating
            reviews: Number of reviews
            address: Business address
        
        Returns:
            Analysis and pitch suggestions
        """
        prompt = f"""Analyze this business and suggest the best pitch angle:

Business: {business_name}
Type: {business_type}
Rating: {rating} stars
Reviews: {reviews}
Location: {address}

Provide:
1. Key strength to mention (1 line)
2. Main pain point they might have (1 line)
3. Best pitch angle for website service (2 lines)

Keep it short and actionable."""

        try:
            response = self.model.generate_content(prompt)
            analysis = response.text.strip()
            logger.info(f"Generated analysis for {business_name}")
            return analysis
        except Exception as e:
            logger.error(f"Gemini AI error: {str(e)}")
            return f"Strong reputation ({rating}★, {reviews} reviews). Missing online presence. Pitch: Professional website to capture online customers."
    
    def _fallback_email(self, business_name: str, business_type: str, 
                       rating: float, reviews: int) -> str:
        """Fallback email template with business analysis."""
        # Determine problems based on business type
        problems = {
            'restaurant': 'no online ordering system and outdated website',
            'cafe': 'no mobile app for orders and weak online presence',
            'retail': 'no e-commerce platform to sell online',
            'salon': 'no online booking system',
            'healthcare': 'no appointment booking system',
            'education': 'no online learning platform',
            'service': 'outdated website and poor SEO'
        }
        
        problem = problems.get(business_type.lower().split()[0], 'limited online presence')
        
        return f"""Hi,

I noticed {business_name} has an excellent reputation with {rating} stars and {reviews} reviews! Your customers clearly love you.

However, I also noticed you have {problem}. In today's digital age, this means you're potentially losing 60-70% of customers who search online before visiting.

I'm Raghav Shah from RagsPro.com - a development agency based in Delhi. We specialize in helping businesses like yours grow online:

• Mobile Apps (iOS/Android) - For easy customer ordering
• Web Applications & SaaS - Modern, fast websites
• E-commerce Solutions - Sell online 24/7
• SEO & Digital Marketing - Get found on Google
• AI Integration - Smart features for modern businesses

We've built successful products like:
- LawAI (legal tech platform)
- Glow (AI photo editor)
- HimShakti (e-commerce platform)

200+ projects delivered | 50+ happy clients | 5★ ratings

For {business_type} businesses, we typically see 3-5x revenue increase within 6 months of going digital.

Would you be interested in a FREE consultation? I can:
✓ Analyze your current online presence
✓ Show you what competitors are doing
✓ Create a custom digital roadmap
✓ Share our portfolio and case studies

No obligation - just professional advice from someone who wants to see your business grow.

Best regards,
Raghav Shah
Founder, Ragspro.com - Software Development Agency

📞 +918700048490
📧 raghav@ragspro.com
🌐 ragspro.com

Connect with me:
💼 LinkedIn: linkedin.com/in/raghavshahhh
💻 GitHub: github.com/raghavshahhhh
📸 Instagram: instagram.com/raghavshahhhh
🎥 YouTube: youtube.com/@raghavshahhh
🐦 Twitter: x.com/raghavshahhhh
💼 Fiverr: fiverr.com/s/WEpRvR7"""
    
    def _fallback_whatsapp(self, business_name: str, business_type: str) -> str:
        """Fallback WhatsApp template with problem identification."""
        # Determine problem based on business type
        problems = {
            'restaurant': 'no online ordering - losing customers',
            'cafe': 'no mobile app - competitors ahead',
            'retail': 'not selling online - missing revenue',
            'salon': 'no online booking - customers going elsewhere',
            'healthcare': 'no appointment system - inefficient',
            'education': 'no online platform - students want digital',
            'service': 'weak online presence - not getting leads'
        }
        
        problem = problems.get(business_type.lower().split()[0], 'limited digital presence')
        
        return f"""Hey! 👋 Raghav from RagsPro.com (Delhi)

Saw {business_name} on Google - great ratings! 🌟

But noticed {problem}. This is costing you 60-70% potential customers who search online first.

We build mobile apps, websites, SaaS for {business_type} businesses. Built LawAI, Glow, HimShakti - 200+ projects delivered! 💻

Typical result: 3-5x revenue increase in 6 months 💰

Want FREE business analysis + digital roadmap? ✅

Reply YES or call +918700048490 📱

Limited slots this month! 🚀"""


def create_ai_assistant(api_key: str) -> GeminiAI:
    """
    Create Gemini AI assistant instance.
    
    Args:
        api_key: Google Gemini API key (FREE tier available)
    
    Returns:
        GeminiAI instance
    """
    return GeminiAI(api_key)
