"""Query generation module for Lead Generation Bot."""

# HIGH-PAYING INTERNATIONAL CITIES (Priority: USA, UK, Dubai, Canada, Australia, Europe)
CITIES = [
    # USA - Top Tier (Highest paying clients - $5000-$50000 projects)
    "New York, USA",
    "San Francisco, USA",
    "Los Angeles, USA",
    "Chicago, USA",
    "Miami, USA",
    "Austin, USA",
    "Seattle, USA",
    "Boston, USA",
    "Dallas, USA",
    "San Diego, USA",
    "Denver, USA",
    "Atlanta, USA",
    
    # UK - Top Tier (High paying - £3000-£30000 projects)
    "London, UK",
    "Manchester, UK",
    "Birmingham, UK",
    "Edinburgh, UK",
    "Bristol, UK",
    
    # UAE - Top Tier (Very high paying - AED 20000-200000 projects)
    "Dubai, UAE",
    "Abu Dhabi, UAE",
    "Sharjah, UAE",
    
    # Canada - Top Tier (High paying - CAD 5000-50000 projects)
    "Toronto, Canada",
    "Vancouver, Canada",
    "Montreal, Canada",
    "Calgary, Canada",
    
    # Australia - Top Tier (High paying - AUD 5000-50000 projects)
    "Sydney, Australia",
    "Melbourne, Australia",
    "Brisbane, Australia",
    "Perth, Australia",
    
    # Singapore - Top Tier (Very high paying - SGD 5000-50000 projects)
    "Singapore",
    
    # Europe - High Tier (Good paying - €3000-€30000 projects)
    "Paris, France",
    "Berlin, Germany",
    "Amsterdam, Netherlands",
    "Zurich, Switzerland",
    "Stockholm, Sweden",
    "Copenhagen, Denmark",
    "Oslo, Norway",
    "Dublin, Ireland",
    
    # Middle East - High Tier (Good paying)
    "Doha, Qatar",
    "Riyadh, Saudi Arabia",
    
    # Asia Pacific - Medium Tier (Decent paying)
    "Hong Kong",
    "Tokyo, Japan",
    "Seoul, South Korea",
    
    # India - Lower Tier (But high volume - ₹50000-₹500000 projects)
    "Mumbai, India",
    "Bangalore, India",
    "Delhi, India",
    "Gurgaon, India",
    "Pune, India",
]

# HIGH-VALUE BUSINESS CATEGORIES (Businesses that pay MAXIMUM for tech services)
# Sorted by average project value (highest to lowest)
CATEGORIES = [
    # Tech & SaaS (HIGHEST payout: $10k-$100k+ projects)
    "software company",
    "tech startup",
    "SaaS company",
    "fintech company",
    "AI company",
    "blockchain company",
    "cybersecurity firm",
    
    # Finance & Investment (HIGHEST payout: $15k-$150k+ projects)
    "investment firm",
    "hedge fund",
    "private equity",
    "venture capital",
    "wealth management",
    "cryptocurrency exchange",
    
    # Professional Services (HIGH payout: $8k-$80k projects)
    "law firm",
    "corporate law firm",
    "accounting firm",
    "consulting firm",
    "management consulting",
    "business consulting",
    "tax advisory",
    
    # Real Estate (HIGH payout: $10k-$100k projects)
    "real estate agency",
    "luxury real estate",
    "commercial real estate",
    "property management",
    "real estate developer",
    
    # Healthcare (HIGH payout: $7k-$70k projects)
    "cosmetic surgery",
    "plastic surgery",
    "dental clinic",
    "medical clinic",
    "fertility clinic",
    "dermatology clinic",
    "veterinary clinic",
    "mental health clinic",
    
    # E-commerce & Retail (GOOD payout: $5k-$50k projects)
    "luxury boutique",
    "jewelry store",
    "watch store",
    "fashion brand",
    "online store",
    "electronics store",
    "furniture store",
    
    # Hospitality & Travel (GOOD payout: $6k-$60k projects)
    "luxury hotel",
    "resort",
    "boutique hotel",
    "travel agency",
    "tour operator",
    "event venue",
    
    # Food & Beverage (MEDIUM-HIGH payout: $4k-$40k projects)
    "fine dining restaurant",
    "restaurant chain",
    "cafe chain",
    "catering company",
    "cloud kitchen",
    
    # Fitness & Wellness (GOOD payout: $5k-$50k projects)
    "luxury spa",
    "wellness center",
    "fitness chain",
    "yoga studio chain",
    "meditation center",
    
    # Education (GOOD payout: $5k-$50k projects)
    "online education platform",
    "coaching institute",
    "language school",
    "business school",
    "certification courses",
    
    # Marketing & Media (HIGH payout: $8k-$80k projects)
    "marketing agency",
    "digital marketing agency",
    "advertising agency",
    "PR agency",
    "media production",
    
    # Manufacturing & B2B (HIGH payout: $10k-$100k projects)
    "manufacturing company",
    "industrial equipment",
    "B2B software",
    "wholesale distributor",
    
    # Home & Lifestyle (MEDIUM payout: $4k-$40k projects)
    "interior design firm",
    "architecture firm",
    "construction company",
    "home automation",
]


def generate_queries() -> list[str]:
    """
    Generate all city × category query combinations.
    
    Returns:
        List of search query strings in format "{category} in {city}"
    """
    queries = []
    for city in CITIES:
        for category in CATEGORIES:
            query = f"{category} in {city}"
            queries.append(query)
    return queries
