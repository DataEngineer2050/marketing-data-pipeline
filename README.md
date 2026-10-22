# 🚀 End-to-End E-Commerce Marketing Data Pipeline

A production-grade, resilient data pipeline designed to ingest, validate, transform, and load high-volume marketing campaign data into a modern data warehouse.

## 📌 Step 1: Data Extraction & Resilient Ingestion
In this initial phase, the pipeline simulates real-world marketing API responses (Google Ads, Facebook Ads, Instagram Ads) and establishes a robust landing zone for raw data.

### 🛠️ Key Features Implemented:
- **Mock Data Generation:** Uses `Faker` and `pandas` to generate high-fidelity e-commerce metrics (clicks, spend, revenue).
- **Production Logging:** Implemented structured file logging (`pipeline.log`) tracking system events, runtime information, and unexpected errors.
- **Data Anomaly Simulation:** Intentionally injects a 5% data corruption rate (negative revenues) to pressure-test downstream validation schemas.

### 🏃‍♂️ How to Run Step 1 Locally:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/DataEngineer2050/marketing-data-pipeline
   cd marketing-data-pipeline
   ```

2. **Install prerequisites:**
   ```bash
   pip install pandas faker
   ```

3. **Execute the extraction layer:**
   ```bash
   python extraction_data.py
   ```
   *This will generate a `raw_data_landing/` directory containing the raw JSON responses and a `pipeline.log` file.*
