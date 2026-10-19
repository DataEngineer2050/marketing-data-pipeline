
import os
import json
import random
import logging
from datetime import datetime, timedelta
import pandas as pd
from faker import Faker

# 1. Logging Setup (Essential for monitoring and alerting in production environments)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log"),  # Redirects and stores runtime logs in a dedicated log file for auditing
        logging.StreamHandler()              # Streams logs directly to the console/terminal
    ]
)

fake = Faker()

# 2. Mock Campaign Data (Static configuration array for marketing campaigns)
CAMPAIGNS = [
    {"campaign_id": "CAMP_001", "campaign_name": "Winter Apparel Blast", "channel": "Google Ads"},
    {"campaign_id": "CAMP_002", "campaign_name": "Summer Clearance 2026", "channel": "Facebook Ads"},
    {"campaign_id": "CAMP_003", "campaign_name": "Sneakers Retargeting", "channel": "Instagram Ads"},
    {"campaign_id": "CAMP_004", "campaign_name": "Tech Gadgets Launch", "channel": "Google Ads"},
]

def generate_mock_api_data(days_of_data=5):
    """
    Simulates a real-world e-commerce marketing API response
    Intentionally injects anomalies to pressure-test downstream validation logic
    """
    logging.info(
        f"Extraction Started: Fetching marketing data for the past {days_of_data} days..."
    )
    
    raw_data = []
    end_date = datetime.today()
    
    try:
        for i in range(days_of_data):
            current_date = (end_date - timedelta(days=i)).strftime('%Y-%m-%d')
            
            for camp in CAMPAIGNS:
                # Normal business metrics
                clicks = random.randint(100, 1500)
                spend = round(random.uniform(50.0, 500.0), 2)
                
                # Real-world scenarios: Simulates a typical 85% conversion rate baseline; remaining instances result in zero conversions
                if random.random() > 0.15:
                    revenue = round(spend * random.uniform(1.2, 4.0), 2)
                else:
                    revenue = 0.0
                
                # PRODUCTION EDGE CASE SIMULATION:
                # Introduces a 5% data corruption threshold (e.g., negative revenue values) for edge-case simulation
                # Implemented to allow downstream schema and validation testing in the next phase
                if random.random() < 0.05:
                    revenue = -100.00  # Corrupt Data Rule 1
                    logging.warning(f"Simulating corrupt data for {camp['campaign_id']} on {current_date}")
                
                data_point = {
                    "date": current_date,
                    "campaign_id": camp["campaign_id"],
                    "campaign_name": camp["campaign_name"],
                    "channel": camp["channel"],
                    "clicks": clicks,
                    "spend": spend,
                    "revenue": revenue
                }
                raw_data.append(data_point)
                
        logging.info(f"Extraction Completed: Successfully generated {len(raw_data)} records.")
        return raw_data

    except Exception as e:
        logging.error(f"Data extraction failed: {str(e)}")
        raise e

if __name__ == "__main__":
    # Initialize data generation process
    extracted_data = generate_mock_api_data(days_of_data=7)
    
    # "Save raw data payload in JSON format as an immutable source backup
    os.makedirs("raw_data_landing", exist_ok=True)
    file_path = f"raw_data_landing/marketing_data_{datetime.today().strftime('%Y%m%d')}.json"
    
    with open(file_path, "w") as f:
        json.dump(extracted_data, f, indent=4)
        
    logging.info(f"Raw API response archive successfully saved: {file_path}")
    
    # Print raw data preview for initial structural verification
    df = pd.DataFrame(extracted_data)
    print("\n--- Extracted Data Preview (First 5 Rows) ---")
    print(df.head())
