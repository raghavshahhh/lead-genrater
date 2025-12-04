"""Main orchestrator for Lead Generation Bot."""

import logging
import os
from datetime import datetime
from pathlib import Path

from src.config import load_config
from src.queries import generate_queries
from src.scraper import search_places
from src.filters import is_good_lead, transform_place
from src.dedupe import load_seen_ids, save_seen_ids
from src.storage import append_to_sheet, append_to_csv


def setup_logging():
    """Set up logging with ISO 8601 timestamps and daily log files."""
    # Create logs directory
    os.makedirs("logs", exist_ok=True)
    
    # Create log filename with date
    log_date = datetime.utcnow().strftime("%Y-%m-%d")
    log_file = f"logs/lead_bot_{log_date}.log"
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)


def run():
    """Execute the complete lead generation workflow."""
    logger = setup_logging()
    logger.info("=" * 80)
    logger.info("Starting Lead Generation Bot")
    logger.info("=" * 80)
    
    try:
        # Load configuration
        logger.info("Loading configuration...")
        config = load_config()
        
        api_key = config["SERPAPI_KEY"]
        sheet_id = config["GOOGLE_SHEET_ID"]
        service_account_file = config["GOOGLE_SERVICE_ACCOUNT_JSON"]
        min_rating = config["MIN_RATING"]
        min_reviews = config["MIN_REVIEWS"]
        max_leads = config["MAX_LEADS_PER_RUN"]
        
        logger.info(f"Configuration loaded: MAX_LEADS={max_leads}, MIN_RATING={min_rating}, MIN_REVIEWS={min_reviews}")
        
        # Load previously processed Place IDs
        logger.info("Loading processed Place IDs...")
        seen_ids = load_seen_ids()
        logger.info(f"Loaded {len(seen_ids)} previously processed Place IDs")
        
        # Generate queries
        logger.info("Generating search queries...")
        queries = generate_queries()
        logger.info(f"Generated {len(queries)} search queries")
        
        # Process queries and collect leads
        qualified_leads = []
        new_place_ids = set()
        
        queries_processed = 0
        total_results = 0
        filtered_out = 0
        duplicates_skipped = 0
        
        for query in queries:
            # Check if we've reached the limit
            if len(qualified_leads) >= max_leads:
                logger.info(f"Reached maximum lead limit ({max_leads}). Stopping query processing.")
                break
            
            logger.info(f"Processing query: {query}")
            
            # Fetch results
            places = search_places(query, api_key)
            total_results += len(places)
            queries_processed += 1
            
            # Filter and transform
            for place in places:
                # Check limit again
                if len(qualified_leads) >= max_leads:
                    break
                
                # Check if it's a good lead
                if not is_good_lead(place):
                    filtered_out += 1
                    continue
                
                # Check for duplicates
                place_id = place.get("place_id", "")
                if place_id in seen_ids or place_id in new_place_ids:
                    duplicates_skipped += 1
                    logger.debug(f"Skipping duplicate Place ID: {place_id}")
                    continue
                
                # Transform and add to qualified leads
                lead = transform_place(place, query)
                qualified_leads.append(lead)
                new_place_ids.add(place_id)
                
                logger.info(f"Qualified lead found: {lead['business_name']} ({lead['city']})")
        
        # Store leads
        logger.info(f"Storing {len(qualified_leads)} qualified leads...")
        
        if qualified_leads:
            # Store to Google Sheets
            try:
                append_to_sheet(qualified_leads, sheet_id, service_account_file)
            except Exception as e:
                logger.error(f"Failed to store leads to Google Sheets: {str(e)}")
            
            # Store to CSV
            append_to_csv(qualified_leads)
            
            # Save new Place IDs
            if new_place_ids:
                all_ids = seen_ids | new_place_ids
                save_seen_ids(all_ids)
        
        # Log execution summary
        logger.info("=" * 80)
        logger.info("Execution Summary:")
        logger.info(f"  Queries processed: {queries_processed}")
        logger.info(f"  Total results found: {total_results}")
        logger.info(f"  Leads filtered out: {filtered_out}")
        logger.info(f"  Duplicates skipped: {duplicates_skipped}")
        logger.info(f"  New leads added: {len(qualified_leads)}")
        logger.info("=" * 80)
        logger.info("Lead Generation Bot completed successfully")
        
        return len(qualified_leads)
        
    except Exception as e:
        logger.error(f"Fatal error in lead generation workflow: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    run()
