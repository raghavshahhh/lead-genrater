"""
Lead Quality Filter - Identifies HIGH-PAYING, SERIOUS clients only.
Filters out tire-kickers and low-budget clients.
"""

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class LeadQualityScorer:
    """Scores leads based on likelihood of being a high-paying, serious client."""
    
    # 🎯 RAGSPRO-SPECIFIC: Software development client indicators
    HIGH_VALUE_KEYWORDS = [
        # Buying signals for dev services (HIGHEST priority)
        "hiring", "looking for", "seeking", "need developer",
        "software partner", "tech team", "engineering",
        "MVP", "product development", "app development",
        
        # Business stage indicators (well-funded)
        "funded", "series A", "series B", "venture backed",
        "raised", "revenue", "profitable", "growth",
        
        # Business size indicators
        "startup", "scale-up", "enterprise", "international",
        "global", "corporate", "group",
        
        # Tech-savvy indicators (good fit)
        "SaaS", "platform", "marketplace", "API",
        "cloud", "mobile app", "web app", "e-commerce",
        "fintech", "AI", "machine learning", "blockchain",
        
        # Professional indicators
        "established", "award-winning", "certified",
        "accredited", "since", "years experience",
    ]
    
    # 🚫 RED FLAGS: Bad clients for software development
    LOW_VALUE_KEYWORDS = [
        # No budget indicators
        "cheap", "budget", "affordable", "discount", "free",
        "equity only", "rev share", "profit share", "no budget",
        "student project", "volunteer", "intern",
        
        # Small/non-serious
        "home-based", "freelance", "solo", "one-man",
        "hobby", "part-time", "side project", "casual",
        
        # Wrong fit
        "looking for freelancer", "quick fix", "small task",
        "one-time", "urgent", "ASAP only",
    ]
    
    # 💰 HIGH-BUDGET CATEGORIES: Best clients for software development
    HIGH_BUDGET_CATEGORIES = [
        # Tech companies (PERFECT fit - always need devs)
        "saas", "software", "tech startup", "platform",
        "fintech", "AI company", "machine learning",
        "blockchain", "cryptocurrency", "web3",
        "marketplace", "e-commerce platform",
        
        # Well-funded industries
        "venture capital", "private equity", "investment",
        "hedge fund", "wealth management",
        
        # Digital-first businesses
        "online education", "edtech", "healthtech",
        "proptech", "insurtech", "legaltech",
        
        # Enterprise
        "enterprise software", "B2B software",
        "consulting firm", "digital agency",
        
        # E-commerce (always optimizing)
        "e-commerce", "online store", "DTC brand",
        "marketplace", "retail tech",
    ]
    
    # Business categories with LOW budgets
    LOW_BUDGET_CATEGORIES = [
        "daycare", "babysitter", "nanny",
        "tutor", "coaching",
        "salon", "barber",
        "laundry", "dry clean",
    ]
    
    @staticmethod
    def calculate_quality_score(business: Dict) -> float:
        """
        Calculate quality score (0-100) for a business lead.
        Higher score = more likely to be high-paying, serious client.
        
        Args:
            business: Business dictionary with title, type, rating, reviews, website
            
        Returns:
            Quality score (0-100)
        """
        score = 50.0  # Start at neutral
        
        title = business.get('title', '').lower()
        business_type = business.get('type', '').lower()
        rating = business.get('rating', 0)
        reviews = business.get('reviews', 0)
        website = business.get('website')
        phone = business.get('phone')
        
        # 1. Check for high-value keywords (+20 points max)
        high_value_count = sum(1 for keyword in LeadQualityScorer.HIGH_VALUE_KEYWORDS 
                               if keyword in title or keyword in business_type)
        score += min(high_value_count * 5, 20)
        
        # 2. Check for low-value keywords (-20 points max)
        low_value_count = sum(1 for keyword in LeadQualityScorer.LOW_VALUE_KEYWORDS 
                              if keyword in title or keyword in business_type)
        score -= min(low_value_count * 10, 20)
        
        # 3. Check business category (+15 or -15 points)
        is_high_budget = any(cat in title or cat in business_type 
                            for cat in LeadQualityScorer.HIGH_BUDGET_CATEGORIES)
        is_low_budget = any(cat in title or cat in business_type 
                           for cat in LeadQualityScorer.LOW_BUDGET_CATEGORIES)
        
        if is_high_budget:
            score += 15
        if is_low_budget:
            score -= 15
        
        # 4. Rating quality (+10 points for excellent rating)
        if rating >= 4.5:
            score += 10
        elif rating >= 4.0:
            score += 5
        elif rating < 3.0 and rating > 0:
            score -= 10
        
        # 5. Review count (indicates established business) (+15 points max)
        if reviews >= 500:
            score += 15
        elif reviews >= 200:
            score += 10
        elif reviews >= 100:
            score += 5
        elif reviews >= 50:
            score += 2
        
        # 6. Has website (+10 points - shows they invest in online presence)
        if website and website.strip():
            score += 10
        else:
            # No website is actually GOOD for us (they need our services!)
            score += 5
        
        # 7. Has phone (+5 points - shows they're reachable)
        if phone and phone.strip():
            score += 5
        
        # Clamp score between 0 and 100
        score = max(0, min(100, score))
        
        return score
    
    @staticmethod
    def is_high_quality_lead(business: Dict, min_score: float = 60.0) -> bool:
        """
        Determine if a business is a high-quality lead.
        
        Args:
            business: Business dictionary
            min_score: Minimum quality score (default: 60)
            
        Returns:
            True if high-quality lead, False otherwise
        """
        score = LeadQualityScorer.calculate_quality_score(business)
        business['quality_score'] = score  # Add score to business dict
        
        return score >= min_score
    
    @staticmethod
    def filter_high_quality_leads(businesses: List[Dict], min_score: float = 60.0) -> List[Dict]:
        """
        Filter list of businesses to only high-quality leads.
        
        Args:
            businesses: List of business dictionaries
            min_score: Minimum quality score
            
        Returns:
            Filtered list of high-quality leads
        """
        high_quality = []
        
        for business in businesses:
            score = LeadQualityScorer.calculate_quality_score(business)
            business['quality_score'] = score
            
            if score >= min_score:
                high_quality.append(business)
                logger.info(f"✅ HIGH QUALITY ({score:.0f}/100): {business['title']}")
            else:
                logger.debug(f"❌ Low quality ({score:.0f}/100): {business['title']}")
        
        logger.info(f"Filtered {len(high_quality)}/{len(businesses)} high-quality leads")
        
        return high_quality
    
    @staticmethod
    def rank_leads_by_quality(businesses: List[Dict]) -> List[Dict]:
        """
        Rank leads by quality score (highest first).
        
        Args:
            businesses: List of business dictionaries
            
        Returns:
            Sorted list (highest quality first)
        """
        # Calculate scores
        for business in businesses:
            if 'quality_score' not in business:
                business['quality_score'] = LeadQualityScorer.calculate_quality_score(business)
        
        # Sort by score (descending)
        ranked = sorted(businesses, key=lambda b: b.get('quality_score', 0), reverse=True)
        
        logger.info(f"Ranked {len(ranked)} leads by quality")
        if ranked:
            logger.info(f"Top lead: {ranked[0]['title']} (score: {ranked[0]['quality_score']:.0f})")
        
        return ranked


def filter_serious_clients_only(businesses: List[Dict]) -> List[Dict]:
    """
    Main function to filter for SERIOUS, HIGH-PAYING clients only.
    
    Args:
        businesses: List of all scraped businesses
        
    Returns:
        List of only serious, high-paying clients
    """
    logger.info(f"🎯 Filtering for SERIOUS, HIGH-PAYING clients from {len(businesses)} leads...")
    
    # Filter high-quality leads (score >= 60)
    high_quality = LeadQualityScorer.filter_high_quality_leads(businesses, min_score=60.0)
    
    # Rank by quality
    ranked = LeadQualityScorer.rank_leads_by_quality(high_quality)
    
    logger.info(f"✅ Found {len(ranked)} SERIOUS, HIGH-PAYING clients")
    
    return ranked


# Example usage
if __name__ == "__main__":
    # Test with sample businesses
    test_businesses = [
        {
            'title': 'Smith & Associates Law Firm',
            'type': 'law firm',
            'rating': 4.8,
            'reviews': 350,
            'website': None,  # No website = opportunity!
            'phone': '+1-555-0100'
        },
        {
            'title': 'Budget Babysitting Services',
            'type': 'daycare',
            'rating': 4.2,
            'reviews': 15,
            'website': 'example.com',
            'phone': '+1-555-0200'
        },
        {
            'title': 'Luxury Real Estate Group',
            'type': 'real estate',
            'rating': 4.9,
            'reviews': 500,
            'website': None,
            'phone': '+1-555-0300'
        }
    ]
    
    # Filter
    serious_clients = filter_serious_clients_only(test_businesses)
    
    print("\n🎯 SERIOUS, HIGH-PAYING CLIENTS:")
    for client in serious_clients:
        print(f"  - {client['title']} (Score: {client['quality_score']:.0f}/100)")
