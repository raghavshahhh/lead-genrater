"""Storage module for persisting leads to Google Sheets and CSV."""

import csv
import os
import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials

logger = logging.getLogger(__name__)


def get_sheet(sheet_id: str, service_account_file: str):
    """
    Authenticate and return Google Sheets worksheet object.
    
    Args:
        sheet_id: Google Sheets document ID
        service_account_file: Path to service account JSON key
    
    Returns:
        gspread Worksheet object
    """
    try:
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            service_account_file, scope
        )
        client = gspread.authorize(creds)
        sheet = client.open_by_key(sheet_id).sheet1
        
        logger.info(f"Successfully connected to Google Sheet: {sheet_id}")
        return sheet
        
    except Exception as e:
        logger.error(f"Failed to connect to Google Sheets: {str(e)}")
        raise


def append_to_sheet(leads: list[dict], sheet_id: str, service_account_file: str) -> None:
    """
    Append lead rows to Google Sheet.
    
    Args:
        leads: List of lead dictionaries
        sheet_id: Google Sheets document ID
        service_account_file: Path to service account JSON key
    """
    if not leads:
        logger.info("No leads to append to Google Sheets")
        return
    
    try:
        sheet = get_sheet(sheet_id, service_account_file)
        
        # Define column order
        columns = [
            "business_name", "category", "city", "state", "country",
            "rating", "reviews_count", "phone", "website_url", "has_website",
            "maps_url", "place_id", "created_at", "source_query", "status"
        ]
        
        # Check if sheet is empty and add headers
        if sheet.row_count == 0 or not sheet.row_values(1):
            sheet.append_row(columns)
            logger.info("Added headers to Google Sheet")
        
        # Convert leads to rows
        rows = []
        for lead in leads:
            row = [lead.get(col, "") for col in columns]
            rows.append(row)
        
        # Append all rows at once
        sheet.append_rows(rows)
        logger.info(f"Successfully appended {len(rows)} leads to Google Sheets")
        
    except Exception as e:
        logger.error(f"Error appending to Google Sheets: {str(e)}")
        # Don't raise - continue execution


def append_to_csv(leads: list[dict], path: str = "data/all_leads.csv") -> None:
    """
    Append leads to local CSV file.
    
    Args:
        leads: List of lead dictionaries
        path: Path to CSV file
    """
    if not leads:
        logger.info("No leads to append to CSV")
        return
    
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Define column order
        columns = [
            "business_name", "category", "city", "state", "country",
            "rating", "reviews_count", "phone", "website_url", "has_website",
            "maps_url", "place_id", "created_at", "source_query", "status"
        ]
        
        # Check if file exists
        file_exists = os.path.exists(path)
        
        # Open file in append mode with UTF-8 encoding
        with open(path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            
            # Write header if file is new
            if not file_exists:
                writer.writeheader()
                logger.info(f"Created new CSV file with headers: {path}")
            
            # Write leads
            for lead in leads:
                writer.writerow(lead)
        
        logger.info(f"Successfully appended {len(leads)} leads to CSV: {path}")
        
    except Exception as e:
        logger.error(f"Error appending to CSV: {str(e)}")
        # Don't raise - continue execution
