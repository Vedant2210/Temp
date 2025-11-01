# Apache JIRA Scraper

> A robust, modular Python-based scraper to collect, process, and transform issue data from **Apache JIRA** projects (like Hadoop, Spark, and Kafka) into structured **JSONL format** — ideal for analytics or LLM training.

---

## Overview

The **Apache JIRA Scraper** automates the extraction of public issue data from Apache’s JIRA system using REST APIs.  
It helps researchers, developers, and data engineers create high-quality datasets by scraping issue descriptions, comments, metadata, and transforming them into a **machine-readable** format.

This tool is designed for:
-  Data collection for ML/NLP research  
-  Issue tracking & project analytics  
-  Training datasets for LLM fine-tuning  

---

## ⚙️ Tech Stack

| Category | Tools / Libraries |
|-----------|-------------------|
| **Language** | Python 3.10+ |
| **HTTP Requests** | `requests` |
| **Data Handling** | `json`, `pandas` |
| **Logging** | `logging`, custom loggers |
| **Configuration** | `argparse`, `settings.py` |
| **Environment** | `venv` |
| **Output Format** | `.jsonl` |
| **Version Control** | Git & GitHub |

---

## 🧩 Features

✅ Fetches issue data from multiple Apache projects (Hadoop, Spark, Kafka, etc.)  
✅ Transforms raw JSON into cleaned `.jsonl` format  
✅ Auto-handles rate limits and retries  
✅ Logs every step for debugging & monitoring  
✅ Checkpoint system for fault tolerance  
✅ Configurable via `config/settings.py`  
✅ Modular and extensible for new data pipelines  

---

## 📁 Project Structure

```bash
apache-jira-scraper/
│
├── config/
│   └── settings.py           # Configuration variables (project list, limits)
│
├── data/
│   ├── raw/                  # Raw JSON data from JIRA API
│   ├── processed/            # Cleaned JSONL files
│   └── checkpoints/          # Track last processed issue ID
│
├── logs/                     # Logging directory
│
├── src/
│   ├── scraper.py            # Core scraper logic
│   ├── transform.py          # Data transformation and saving
│   └── logger.py             # Logging setup
│
├── main.py                   # Entry point for the scraper
├── requirements.txt          # Dependencies list
└── README.md                 # Project documentation
```
## ⚙️ Configuration

All configuration variables are stored in **`config/settings.py`**.  
Below is a table describing each key configuration parameter:

| Variable Name       | Description                                              | Example Value                                                |
|----------------------|----------------------------------------------------------|--------------------------------------------------------------|
| `PROJECTS`           | List of Apache project names to scrape                   | `["HADOOP", "SPARK", "KAFKA"]`                              |
| `ISSUE_FETCH_LIMIT`  | Maximum number of issues to fetch per project            | `500`                                                        |
| `OUTPUT_DIR`         | Directory to store processed JSONL files                 | `"data/processed/"`                                          |
| `LOG_FILE`           | Path to the log file for tracking scraping progress      | `"logs/scraper.log"`                                         |
| `BASE_URL`           | Base URL of the Apache JIRA server                       | `"https://issues.apache.org/jira/rest/api/2/search"`         |

## ⚙️ Installation & Setup

Follow these steps to set up and run the scraper locally 👇

---

### 1️⃣ Clone the Repository

```
git clone https://github.com/Vedant2210/Apache_Jira_Scraper.git
cd Apache_Jira_Scraper
```
2️⃣ Create a Virtual Environment
```
python -m venv venv
```
3️⃣ Activate the Virtual Environment
Windows:
```
venv\Scripts\activate
```
macOS/Linux:
```
source venv/bin/activate
```
4️⃣ Install Dependencies
```
pip install -r requirements.txt
```
5️⃣ Verify Installation
To ensure Python and pip are correctly installed, run:
```
python --version
pip --version
```
Expected output example:
```
nginx

Python 3.10.x
pip 23.x.x
```
▶️ Usage Guide
Once setup is complete, run the scraper:
```
python main.py
```
This will start fetching issue data for all projects listed inside your config/settings.py file.

By default, the projects are:
```
DEFAULT_PROJECTS = ["HADOOP", "SPARK", "KAFKA"]
```
Each project’s issue data will be scraped, transformed, and saved in .jsonl format under the data/processed directory.





Output Format

All processed issues are stored in:
```
data/processed/{project_name}_issues.jsonl
```
Example:
```
{"id": "HADOOP-1001", "summary": "Fix namenode error", "status": "Open", "reporter": "user123"}
{"id": "SPARK-2020", "summary": "Improve shuffle performance", "status": "Closed", "reporter": "dev456"}
```
🪵 Logging

Logs are automatically generated to help you monitor scraping progress and errors.
All logs are stored in the path specified in settings.py (default: logs/scraper.log).

Example log entry:
```
[2025-11-01 14:25:37] INFO: Fetched 100 issues from project HADOOP
[2025-11-01 14:26:12] WARNING: Failed to fetch issue SPARK-998 (Timeout)
```
### 🧩 Project Pipeline Overview

| Step | Description | File / Module | Output / Notes |
|------|--------------|----------------|----------------|
| 1️⃣ | **Start the main script** | `main.py` | Initializes the pipeline |
| 2️⃣ | **Load configuration settings** | `config/settings.py` | Loads parameters and credentials |
| 3️⃣ | **Fetch issues from Jira** | `scraper.py` (class: `JiraScraper`) | Retrieves issues via API |
| 4️⃣ | **Handle pagination, rate limits, and retries** | `scraper.py` | Ensures all pages are fetched reliably |
| 5️⃣ | **Save raw JSON data** | `data/raw/` | Stores unprocessed API responses |
| 6️⃣ | **Clean and transform data** | `transform.py` (class: `DataTransformer`) | Formats and preprocesses data |
| 7️⃣ | **Generate JSONL formatted output** | `transform.py` | Produces structured JSONL |
| 8️⃣ | **Save processed data** | `data/processed/` | Stores final cleaned dataset |
| 9️⃣ | **Log progress and status** | `logs/*.log` | Keeps track of run details |
| 🔟 | **End of pipeline** | — | Process completed successfully |

---

### 🧩 End-to-End Workflow

| Step | Description | File / Module | Output / Notes | Checkpoint |
|------|--------------|----------------|----------------|-------------|
| 1️⃣ | **Start the pipeline** | `main.py` | Initializes all modules and loggers | — |
| 2️⃣ | **Load configuration settings** | `config/settings.py` | Loads API tokens, Jira URLs, and output paths | `.checkpoint_config` |
| 3️⃣ | **Fetch issues from Jira** | `scraper.py` (class: `JiraScraper`) | Collects raw issues using API requests | `.checkpoint_scraper` |
| 4️⃣ | **Handle pagination, rate limits, and retries** | `scraper.py` | Ensures reliable, complete data fetching | Integrated |
| 5️⃣ | **Save raw JSON data** | `data/raw/` | Saves raw unprocessed data | `.checkpoint_raw` |
| 6️⃣ | **Clean and transform data** | `transform.py` (class: `DataTransformer`) | Applies cleaning, formatting, deduplication | `.checkpoint_transformer` |
| 7️⃣ | **Generate JSONL output** | `transform.py` | Creates structured JSONL file for downstream tasks | `.checkpoint_jsonl` |
| 8️⃣ | **Save processed data** | `data/processed/` | Final cleaned and validated dataset | `.checkpoint_processed` |
| 9️⃣ | **Log progress** | `logs/*.log` | Tracks each step and any exceptions | Auto |
| 🔟 | **Resume from last checkpoint (if rerun)** | `main.py` | Skips completed stages automatically | — |
| ✅ | **End of pipeline** | — | Successfully completed workflow | — |
