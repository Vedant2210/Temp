import json
import os
import argparse

def parse_issue(issue):
    fields = issue.get("fields", {})
    return {
        "project": fields.get("project", {}).get("key"),
        "issue_key": issue.get("key"),
        "title": fields.get("summary"),
        "status": fields.get("status", {}).get("name"),
        "reporter": fields.get("reporter", {}).get("displayName"),
        "assignee": fields.get("assignee", {}).get("displayName") if fields.get("assignee") else None,
        "priority": fields.get("priority", {}).get("name") if fields.get("priority") else None,
        "labels": fields.get("labels", []),
        "created": fields.get("created"),
        "updated": fields.get("updated"),
        "description": fields.get("description"),
        "comments": [
            {"author": c["author"]["displayName"], "body": c["body"]}
            for c in fields.get("comment", {}).get("comments", [])
        ],
        "derived_tasks": {
            "summarization": fields.get("summary"),
            "classification": "bug" if "bug" in fields.get("labels", []) else "feature",
            "qna": {
                "question": f"What is the issue '{fields.get('summary')}' about?",
                "answer": fields.get("description")
            }
        }
    }

def transform_to_jsonl(input_dir, output_file):
    with open(output_file, "w", encoding="utf-8") as out_f:
        for filename in os.listdir(input_dir):
            if not filename.endswith(".json"):
                continue
            with open(os.path.join(input_dir, filename), "r", encoding="utf-8") as f:
                data = json.load(f)
                for issue in data:
                    json.dump(parse_issue(issue), out_f)
                    out_f.write("\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="data/raw")
    parser.add_argument("--output", default="output/apache_issues.jsonl")
    args = parser.parse_args()

    os.makedirs("output", exist_ok=True)
    transform_to_jsonl(args.input_dir, args.output)
