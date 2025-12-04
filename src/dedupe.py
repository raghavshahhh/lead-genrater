"""Deduplication module for tracking processed Place IDs."""

import os
import logging

logger = logging.getLogger(__name__)


def load_seen_ids(path: str = "data/processed_ids.txt") -> set[str]:
    """
    Load previously processed Place IDs from file.
    
    Args:
        path: Path to the processed IDs file
    
    Returns:
        Set of Place IDs that have been processed
    """
    if not os.path.exists(path):
        logger.info(f"Processed IDs file not found: {path}. Starting with empty set.")
        return set()
    
    try:
        with open(path, 'r') as f:
            ids = {line.strip() for line in f if line.strip()}
        logger.info(f"Loaded {len(ids)} processed Place IDs from {path}")
        return ids
    except Exception as e:
        logger.error(f"Error loading processed IDs from {path}: {str(e)}")
        return set()


def save_seen_ids(ids: set[str], path: str = "data/processed_ids.txt") -> None:
    """
    Save Place IDs to file (appending new ones).
    
    Args:
        ids: Set of Place IDs to save
        path: Path to the processed IDs file
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Load existing IDs
        existing_ids = load_seen_ids(path)
        
        # Find new IDs
        new_ids = ids - existing_ids
        
        if new_ids:
            # Append new IDs
            with open(path, 'a') as f:
                for place_id in new_ids:
                    f.write(f"{place_id}\n")
            logger.info(f"Saved {len(new_ids)} new Place IDs to {path}")
        else:
            logger.info("No new Place IDs to save")
            
    except Exception as e:
        logger.error(f"Error saving processed IDs to {path}: {str(e)}")
