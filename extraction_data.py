
import os
import json
import random
import logging
from datetime import datetime, timedelta
import pandas as pd
from faker import Faker

# 1. Logging Setup (Production mein alerts aur tracking ke liye zaroori hai)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log"),  # Logs file mein save honge
        logging.StreamHandler()              # Logs terminal par bhi dikhenge
    ]
)

fake = Faker()

# 2. Mock Campaign Data (Campaigns ki static list)
CAMPAIGNS = [
    {"campaign_id": "CAMP_001", "campaign_name": "Winter Apparel Blast", "channel": "Google Ads"},
    {"campaign_id": "CAMP_002", "campaign_name": "Summer Clearance 2026", "channel": "Facebook Ads"},
    {"campaign_id": "CAMP_003", "campaign_name": "Sneakers Retargeting", "channel": "Instagram Ads"},
    {"campaign_id": "CAMP_004", "campaign_name": "Tech Gadgets Launch", "channel": "Google Ads"},
]

def generate_mock_api_data(days_of_data=5):
    """
    Real-world API data response ko simulate karta hai.
    Janbujh kar kuch kharab data (corrupt data) bhi inject karega taaki step 2 mein test ho sake.
    """
    logging.info(
        f"Extraction Shuru: Pichle {days_of_data} dinon ka data fetch kiya ja raha hai..."
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
                
                # Real-world scenarios: 85% time profit hoga, kuch time conversions nahi hongi
                if random.random() > 0.15:
                    revenue = round(spend * random.uniform(1.2, 4.0), 2)
                else:
                    revenue = 0.0
                
                # PRODUCTION EDGE CASE SIMULATION:
                # 5% chances hain ki data corrupt ho jaye (e.g., negative revenue ya missing data)
                # Taaki hum agle step mein validation test kar sakein
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
                
        logging.info(f"Extraction Mukammal: Total {len(raw_data)} records generate hue.")
        return raw_data

    except Exception as e:
        logging.error(f"Data extract karne mein error aaya: {str(e)}")
        raise e

if __name__ == "__main__":
    # Data generate karein
    extracted_data = generate_mock_api_data(days_of_data=7)
    
    # Raw data ko JSON format mein save karna (Aksar Data Engineering mein raw response backup rakha jata hai)
    os.makedirs("raw_data_landing", exist_ok=True)
    file_path = f"raw_data_landing/marketing_data_{datetime.today().strftime('%Y%m%d')}.json"
    
    with open(file_path, "w") as f:
        json.dump(extracted_data, f, indent=4)
        
    logging.info(f"Raw API Response backup save ho gaya: {file_path}")
    
    # Sirf check karne ke liye output dekhein
    df = pd.DataFrame(extracted_data)
    print("\n--- Extracted Data Preview (First 5 Rows) ---")
    print(df.head())
