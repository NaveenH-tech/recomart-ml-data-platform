# Recomart Data Ingestion Engine & Storage Layer (Tasks 2 & 3)

A highly scalable, production-ready data ingestion pipeline built following the **Single Responsibility Principle (SRP)**. The system handles modular extraction routines for local CSV datasets and external REST API integrations, tracking workflows through structured JSON audit logs, and staging payloads into an organized local Data Lake.

---

## 🏛️ Project Directory Structure

The system enforces a clean, modular hierarchy dividing configurations, utilities, structural source targets, and multi-tier destination directories:

```text
recomart-ml-data-platform/
│
├── config/
│   └── config.yaml            # Central pipeline parameters & dataset path definitions
│
├── data/
│   ├── source/                # Landing pad for incoming/unprocessed source files
│   │   ├── users.csv
│   │   ├── products.csv
│   │   ├── reviews.csv
│   │   ├── sessions.csv
│   │   └── clickstream.csv
│   │
│   ├── raw/                   # Internal Data Lake: Partitioned business objects
│   │   └── [dataset_name]/[YYYY-MM-DD]/[dataset_name].csv
│   │
│   └── external/              # External Data Lake: Vendor API response stream drops
│       └── [api_name]/[YYYY-MM-DD]/[api_name].json
│
├── logs/                      # Audit trails destination
│   └── ingestion.log
│
└── src/
    ├── common/
    │   ├── __init__.py
    │   ├── config.py          # Dynamic absolute path YAML loader
    │   └── logger.py          # Structured JSON log formatter
    │
    └── ingestion/
        ├── __init__.py
        ├── csv_ingestor.py    # Class: Read CSV -> Memory (Pandas DataFrame)
        ├── api_ingestor.py    # Class: HTTP GET -> JSON with Timeout & Retries
        ├── raw_storage.py     # Class: Data Lake Storage Manager
        └── run_ingestion.py   # The Conductor: Orchestration & Routine Execution
```

---

## 🛠️ Setup & Installation

### 1. Install Dependencies
Ensure you have Python 3.10+ installed. Install required packages using `pip`:
```bash
pip install -r requirements.txt
```

### 2. Populate Source Data
Place your source files (`users.csv`, `products.csv`, etc.) inside the `data/source/` directory as specified in `config/config.yaml`.

---

## 🚀 Execution & Automation

Run the master orchestrator script directly from your project root folder:
```bash
python src/ingestion/run_ingestion.py
```

### 🕒 Periodic Automation
Because the pipeline reads parameters dynamically from a standalone configuration file and runs via a single master execution script, it can be scheduled periodically using native system schedulers without altering code:
*   **Linux/macOS (Cron):** Schedule a cronjob (`crontab -e`) to execute the runner daily or hourly.
*   **Windows (Task Scheduler):** Point a Basic Task action directly to your Python executable and pass `src/ingestion/run_ingestion.py` as an argument.

---

## 📦 Core Architecture & Feature Matrix

### 🔄 Data Collection & Ingestion (Task 2)
*   **Multi-Source Processing:** Extracts internal application tables via local CSV streams and calls public web servers using explicit REST connectors.
*   **Resiliency Layer:** The `APIIngestor` features standard network timeouts (`30s`) and defensive error-catching. It automatically handles failure points via a **Max Retries loop** backed by an **Exponential Backoff mechanism** (`time.sleep(2 ** attempt)`).
*   **Defensive Loops:** The orchestrator runs individual extraction jobs inside isolated blocks. If one dataset or URL crashes, the engine logs the event and safely continues processing the next dataset.

### 💾 Raw Data Storage Layer (Task 3)
*   **Logical Partitioning:** Payloads are isolated by data origin bounds. Tabular file conversions are mapped to `data/raw/` while raw JSON API outputs drop under `data/external/`.
*   **Temporal Partitions:** The `RawStorage` system reads files and appends automated, chronological subdirectories using the `YYYY-MM-DD` execution date.

### 📝 Audit Trails & Monitoring
All activities yield machine-readable, single-line **Structured JSON Logs** to standard output. This layout ensures logs are instantly parseable by modern log-management stacks (e.g., Datadog, ELK, AWS CloudWatch).

#### Log Format Sample:
```json
{"timestamp": "2026-07-13T17:08:28.701552+00:00", "level": "INFO", "logger": "data_ingestion", "message": "Ingestion cycle complete.", "pipeline_step": "COMPLETE"}
PS C:\Users\mrudh\BITS WILP\Assignments\Sem 2\DMML\recomart-ml-data-platform> & C:\Users\mrudh\AppData\Local\Microsoft\WindowsApps\python3.12.exe "c:/Users/mrudh/BITS WILP/Assignments/Sem 2/DMML/recomart-ml-data-platform/src/ingestion/run_ingestion.py"
{"timestamp": "2026-07-13T17:09:09.818337+00:00", "level": "INFO", "logger": "data_ingestion", "message": "Conductor initializing with metrics tracking...", "pipeline_step": "START"}
{"timestamp": "2026-07-13T17:09:09.820344+00:00", "level": "INFO", "logger": "data_ingestion", "message": "Reading CSV file into memory: users.csv", "pipeline_step": "CSV_EXTRACT"}
{"timestamp": "2026-07-13T17:09:09.857395+00:00", "level": "INFO", "logger": "data_ingestion", "message": "Saved 3,000 rows to data\\raw\\users\\2026-07-13\\users.csv", "pipeline_step": "RAW_SAVE"}
{"timestamp": "2026-07-13T17:09:09.857395+00:00", "level": "INFO", "logger": "data_ingestion", "message": "Reading CSV file into memory: products.csv", "pipeline_step": "CSV_EXTRACT"}
{"timestamp": "2026-07-13T17:09:09.883245+00:00", "level": "INFO", "logger": "data_ingestion", "message": "Saved 728 rows to data\\raw\\products\\2026-07-13\\products.csv", "pipeline_step": "RAW_SAVE"}
{"timestamp": "2026-07-13T17:09:09.885314+00:00", "level": "INFO", "logger": "data_ingestion", "message": "Reading CSV file into memory: reviews.csv", "pipeline_step": "CSV_EXTRACT"}
{"timestamp": "2026-07-13T17:09:09.925017+00:00", "level": "INFO", "logger": "data_ingestion", "message": "Saved 6,327 rows to data\\raw\\reviews\\2026-07-13\\reviews.csv", "pipeline_step": "RAW_SAVE"}
{"timestamp": "2026-07-13T17:09:09.925017+00:00", "level": "INFO", "logger": "data_ingestion", "message": "Reading CSV file into memory: sessions.csv", "pipeline_step": "CSV_EXTRACT"}
{"timestamp": "2026-07-13T17:09:09.992183+00:00", "level": "INFO", "logger": "data_ingestion", "message": "Saved 15,000 rows to data\\raw\\sessions\\2026-07-13\\sessions.csv", "pipeline_step": "RAW_SAVE"}
{"timestamp": "2026-07-13T17:09:09.993078+00:00", "level": "INFO", "logger": "data_ingestion", "message": "Reading CSV file into memory: clickstream.csv", "pipeline_step": "CSV_EXTRACT"}
{"timestamp": "2026-07-13T17:09:10.404889+00:00", "level": "INFO", "logger": "data_ingestion", "message": "Saved 122,114 rows to data\\raw\\clickstream\\2026-07-13\\clickstream.csv", "pipeline_step": "RAW_SAVE"}
{"timestamp": "2026-07-13T17:09:10.404889+00:00", "level": "INFO", "logger": "data_ingestion", "message": "Initiating HTTP GET request to endpoint: https://dummyjson.com/products", "pipeline_step": "API_EXTRACT"}
{"timestamp": "2026-07-13T17:09:10.649688+00:00", "level": "INFO", "logger": "data_ingestion", "message": "Saved JSON payload response out to data\\external\\products_api\\2026-07-13\\products_api.json", "pipeline_step": "EXTERNAL_SAVE"}

==================================================
 PIPELINE INGESTION SUMMARY
==================================================
🔹 CSV datasets processed : 5
🔹 API datasets processed : 1
🔹 Total records ingested : 147,199
🔹 Processing failures   : 0
🔹 Total execution time  : 0.84 sec
==================================================

{"timestamp": "2026-07-13T17:09:10.649688+00:00", "level": "INFO", "logger": "data_ingestion", "message": "Ingestion cycle complete.", "pipeline_step": "COMPLETE"}
```
