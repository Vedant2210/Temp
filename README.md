# Temp
Web Scraping Tutor

🕸️ Apache Jira Scraper

🚀 A scalable, fault-tolerant web scraping pipeline to extract and transform Apache Jira issue data into structured JSONL format suitable for LLM training.

🧩 Overview

This project automates the extraction of public issue data from Apache’s Jira instance and transforms it into a clean dataset for Large Language Model (LLM) training or downstream NLP tasks.

It was developed as part of the Scaler Web Scraping Assignment to demonstrate:

Resilient API scraping with rate-limit handling

Data checkpointing and recovery

Structured data transformation into JSONL corpus

Logging and error handling for large-scale scraping

🎯 Objective

The system is designed to:

Scrape issues (titles, descriptions, comments, metadata) from multiple Apache Jira projects.

Handle real-world issues like network failures, rate limits, and timeouts.

Resume automatically from the last successful checkpoint if interrupted.

Transform data into structured JSONL format ready for machine learning pipelines.

🧠 Features
Feature	Description
🧾 Multi-Project Scraping	Fetches issues from multiple Apache projects (HADOOP, SPARK, KAFKA)
🔁 Pagination & Checkpoints	Automatically handles paginated API calls and resumes from checkpoints
⚡ Exponential Backoff Retries	Retries failed requests intelligently to avoid hammering the API
🧱 Fault-Tolerant Design	Handles network drops, malformed data, and HTTP 429 / 5xx gracefully
🧹 JSONL Transformation	Converts unstructured Jira data into clean JSONL lines
🪵 Centralized Logging	All activities logged under the /logs folder
💾 Modular Architecture	Configurable settings via config/settings.py
🏗️ Architecture Overview
apache-jira-scraper/
│
├── main.py                  # Entry point for the scraper pipeline
├── config/
│   └── settings.py          # Configurations (URLs, limits, paths)
│
├── src/
│   ├── scraper.py           # JiraScraper class (fetching issues)
│   ├── transform.py         # DataTransformer class (JSONL processing)
│   ├── utils.py             # Helper functions (checkpointing, file ops)
│   └── logger.py            # Custom logging setup
│
├── data/
│   ├── raw/                 # Raw API JSON responses
│   ├── processed/           # Final processed JSONL outputs
│   └── checkpoints/         # Resume states for each project
│
└── logs/                    # Log files

⚙️ Setup Instructions
1️⃣ Clone the Repository
git clone https://github.com/YOUR_GITHUB_USERNAME/apache-jira-scraper.git
cd apache-jira-scraper

2️⃣ Create a Virtual Environment
python -m venv venv
venv\Scripts\activate     # On Windows
# or
source venv/bin/activate  # On macOS/Linux

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Settings (optional)

Edit config/settings.py to adjust:

Projects list (DEFAULT_PROJECTS)

Rate limit delays

Max issues per project

Save paths

5️⃣ Run the Scraper
python main.py

📊 Output
🗂️ Raw Data

Raw JSON data for each project is saved in:

/data/raw/{PROJECT_NAME}_{offset}.json

🧮 Processed JSONL

Final LLM-ready data is stored in:

/data/processed/{PROJECT_NAME}_processed.jsonl


Each line in .jsonl contains one JSON object like:

{
  "project": "HADOOP",
  "key": "HADOOP-12345",
  "title": "Improve shuffle performance in MapReduce",
  "status": "Closed",
  "description": "Detailed explanation of the shuffle bottleneck...",
  "comments": ["This patch improves...", "Merged in r1234"],
  "created": "2024-07-01T10:12:00.000+0000",
  "updated": "2024-07-05T11:30:00.000+0000",
  "labels": ["performance", "optimization"]
}

🧰 Key Concepts Implemented

✅ REST API integration with Apache Jira

✅ Rate limit handling (429) and backoff strategies

✅ Checkpoint-based recovery

✅ Structured data transformation

✅ Clean modular OOP design

✅ Extensive logging system

✅ Configurable constants for scalability

🧱 Error Handling Strategies
Case	Solution
Network failure	Exponential backoff retry mechanism
API rate limit (429)	Graceful wait with retry
5xx server errors	Automatic retry with delay
Incomplete run	Checkpoint reload resumes last position
Empty/malformed JSON	Skipped and logged without crashing
