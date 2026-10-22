import json
import os
import logging
from datetime import datetime
import pandas as pd
from pydantic import BaseModel, Field, field_validator

# --- LOGGING SETUP (As you specified) ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)

# This is your MarketingRecord class 
class MarketingRecord(BaseModel):
    date: str
    campaign_id: str
    campaign_name: str
    channel: str
    clicks: int = Field(..., ge=0)   # Rule: Clicks 0 ya us se zyada hone chahiye
    spend: float = Field(..., ge=0.0) # Rule: Spend negative nahi ho sakta
    revenue: float                    # Isko custom validator se check karenge

    # Custom Rule: If revenue is negative, throw an error
    @field_validator('revenue')
    @classmethod
    def check_positive_revenue(cls, value: float) -> float:
        if value < 0:
            raise ValueError("Negative revenue alert! Data quality issue detected.")
        return value


def transform_and_validate_data(file_path):
    logging.info(f"Transformation shuru: File padhi ja rahi hai -> {file_path}")
    
    # Check if the file actually exists
    if not os.path.exists(file_path):
        logging.error(f"File nahi mili: {file_path}")
        return None

    # Reading the JSON file
    with open(file_path, "r") as f:
        raw_records = json.load(f)

    valid_records = []
    rejected_count = 0

    # Filtering out bad data (Drop bad data)
    for record in raw_records:
        try:
            validated_record = MarketingRecord(**record)
            valid_records.append(validated_record.model_dump())
        except Exception as e:
            rejected_count += 1
            logging.warning(f"Record reject ho gaya! Campaign: {record.get('campaign_id')}")

    logging.info(f"Validation mukammal: {len(valid_records)} pass, {rejected_count} reject.")

    if not valid_records:
        logging.error("Koi bhi sahi data nahi bacha!")
        return None

    # Using Pandas: Converting data into Table format and calculating ROAS(revenue on Ad spend)
    df = pd.DataFrame(valid_records)
    
    # ROAS Calculation (Revenue / Spend). Logic to avoid error if Spend is 0:
    df['roas'] = df.apply(lambda row: round(row['revenue'] / row['spend'], 2) if row['spend'] > 0 else 0.0, axis=1)
    df['date'] = pd.to_datetime(df['date']) # Date ko computer format mein badalna

    return df


if __name__ == "__main__":
    #Finding the file name according to today's date
    today_str = datetime.today().strftime('%Y%m%d')
    input_file = f"raw_data_landing/marketing_data_{today_str}.json"
    
    # Calling the function to process data
    cleaned_df = transform_and_validate_data(input_file)
    
    # If the data is successfully cleaned, save it to a CSV file
    if cleaned_df is not None:
        os.makedirs("clean_data_staging", exist_ok=True)
        output_file = f"clean_data_staging/cleaned_marketing_{today_str}.csv"
        cleaned_df.to_csv(output_file, index=False)
        
        logging.info(f"Sahi data is file mein save ho gaya: {output_file}")
        print("\n--- Cleaned Data Preview ---")
        print(cleaned_df.head()) # Displaying the first 5 lines on the terminal
