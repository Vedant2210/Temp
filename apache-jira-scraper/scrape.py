# import requests
# import os
# import argparse
# import json
# from tqdm import tqdm
# import logging
# from utils import save_json, load_checkpoint, save_checkpoint, retry_request

# BASE_URL = "https://issues.apache.org/jira/rest/api/2/search"

# def fetch_issues(project_key, max_results=500):
#     session = requests.Session()
#     start_at = load_checkpoint(project_key)
#     all_issues = []

#     logging.info(f"Fetching issues for project {project_key}")

#     while True:
#         url = f"{BASE_URL}?jql=project={project_key}&startAt={start_at}&maxResults=50"
#         response = retry_request(session, url)

#         if not response:
#             logging.error("Failed to fetch data after retries.")
#             break

#         data = response.json()
#         issues = data.get("issues", [])
#         if not issues:
#             break

#         all_issues.extend(issues)
#         save_json(f"data/raw/{project_key}_{start_at}.json", issues)
#         save_checkpoint(project_key, start_at)

#         start_at += 50
#         if start_at >= max_results:
#             break

#     return all_issues

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--projects", nargs="+", required=True)
#     parser.add_argument("--max-issues", type=int, default=500)
#     args = parser.parse_args()

#     os.makedirs("data/raw", exist_ok=True)
#     for project in args.projects:
#         fetch_issues(project, args.max_issues)


import requests
import time
import logging
import json
from pathlib import Path

BASE_URL = "https://issues.apache.org/jira/rest/api/2/search"
SAVE_STATE_FILE = "scrape_state.json"

def fetch_issues(project_key, max_issues=100):
    logging.info(f"Fetching issues for project {project_key}")

    issues = []
    start_at = 0
    page_size = 50
    total = None

    # Resume from last saved state
    last_state = load_last_state(project_key)
    if last_state:
        start_at = last_state.get("last_start", 0)
        logging.info(f"Resuming from start={start_at}")

    while True:
        try:
            params = {
                "jql": f"project={project_key}",
                "startAt": start_at,
                "maxResults": page_size,
                "fields": [
                    "summary", "status", "assignee", "reporter", "priority",
                    "labels", "description", "comment", "created", "updated"
                ]
            }

            response = requests.get(BASE_URL, params=params, timeout=15)
            
            # Handle rate limit
            if response.status_code == 429:
                logging.warning("Rate limited. Sleeping for 60 seconds...")
                time.sleep(60)
                continue
            
            response.raise_for_status()
            data = response.json()

            if total is None:
                total = data.get("total", 0)
            
            fetched = data.get("issues", [])
            if not fetched:
                logging.info("No more issues found.")
                break

            for issue in fetched:
                parsed_issue = parse_issue(issue, project_key)
                issues.append(parsed_issue)

            start_at += len(fetched)
            save_last_state(project_key, start_at)

            logging.info(f"Fetched {len(issues)} / {total} issues")

            if start_at >= total or len(issues) >= max_issues:
                break

            time.sleep(2)  # polite delay

        except (requests.RequestException, json.JSONDecodeError) as e:
            logging.error(f"Error fetching data: {e}")
            time.sleep(10)
            continue

    return issues


def load_last_state(project_key):
    if Path(SAVE_STATE_FILE).exists():
        with open(SAVE_STATE_FILE, "r") as f:
            data = json.load(f)
            return data.get(project_key)
    return None

def save_last_state(project_key, start_at):
    data = {}
    if Path(SAVE_STATE_FILE).exists():
        with open(SAVE_STATE_FILE, "r") as f:
            data = json.load(f)
    data[project_key] = {"last_start": start_at}
    with open(SAVE_STATE_FILE, "w") as f:
        json.dump(data, f, indent=2)
