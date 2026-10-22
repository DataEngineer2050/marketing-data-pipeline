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


# 📌 Step 2: Data Transformation & Validation

In this phase of the pipeline, we ingest the raw data generated in Step 1, clean it, validate it against strict production rules, and transform it to make it analysis-ready. 

In production environments, enforcing **Data Quality Checks** before loading data into a data warehouse is a vital practice known as **Data Governance**. This prevents corrupt or malformed data from polluting your downstream tables.

---

## 🛠️ Key Features Implemented

*   **Data Governance & Quality Checks:** Leverages `Pydantic` models to enforce schema validation, ensuring data types (Integers, Floats, Strings) perfectly match specifications.
*   **Production-Grade Exception Handling:** If a record is corrupt, the pipeline catches the error, logs it as a warning, and continues processing the rest of the batch without crashing.
*   **Feature Engineering (ROAS Calculation):** Automatically calculates **ROAS (Return on Ad Spend)** while gracefully handling edge cases like division by zero if `spend` equals zero.

---

## 📋 Validation & Governance Rules

The following quality thresholds are enforced on incoming data batches:
1.  **Clicks Verification:** Total clicks must be a positive integer or zero (`>= 0`).
2.  **Spend Verification:** Total advertising spend cannot be negative (`>= 0.0`).
3.  **Revenue Validation:** A custom business-logic validator intercepts and rejects any negative revenue anomalies (filtering out the 5% intentional data corruption from Step 1).

---

## 🏃‍♂️ How to Run Step 2 Locally

### 1. Install Prerequisites
Install the required libraries needed for data transformation and data validation:
```bash
pip install pandas pydantic
```

### 2. Execute the Transformation Layer
Make sure Step 1 has been executed and today's raw JSON response exists inside the `raw_data_landing/` directory. Then, run the transformation script:
```bash
python transform_data.py
```

---

## 📂 Expected Output

After a successful script execution, the pipeline generates the following assets:

1.  **Staging Layer Folder:** A new `clean_data_staging/` directory is created containing the verified and clean data stored as a **CSV file** (`cleaned_marketing_YYYYMMDD.csv`).
2.  **Consolidated Logs:** The root `pipeline.log` file is updated with metrics showing exactly how many records passed validation and how many rows were rejected.
3.  **Terminal Preview:** Displays a console log preview of the final dataset containing the newly calculated `roas` metrics.

   
   ```
   *This will generate a `raw_data_landing/` directory containing the raw JSON responses and a `pipeline.log` file.*
