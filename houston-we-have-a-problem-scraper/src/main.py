import json
import os
from analyzers.pattern_detector import PatternDetector
from analyzers.validation_rules import ValidationRules
from analyzers.error_logger import ErrorLogger
from outputs.issue_exporter import IssueExporter
from config.settings import SETTINGS_PATH

def load_urls(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def main():
    with open(SETTINGS_PATH, "r") as config_file:
        settings = json.load(config_file)

    urls = load_urls(settings.get("url_list", "data/urls.txt"))

    detector = PatternDetector(settings)
    rules = ValidationRules(settings)
    logger = ErrorLogger(settings)
    exporter = IssueExporter(settings)

    all_issues = []

    for url in urls:
        try:
            print(f"Scanning {url}...")
            page_data = detector.fetch_data(url)
            issues = rules.check(page_data)
            for issue in issues:
                issue_record = logger.log_issue(url, issue)
                all_issues.append(issue_record)
        except Exception as e:
            logger.log_error(url, str(e), severity="high")

    exporter.export(all_issues)
    print(f"Scan complete. Exported {len(all_issues)} issues.")

if __name__ == "__main__":
    main()