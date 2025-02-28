# APACHE_CAMEL_ISSUES_WEB_CRAWLER

The **Apache Camel Issues Web Crawler** is a Python-based automated tool designed to extract, parse and store Apache Camel Issues in a csv file

---


## Installation

### Prerequisites


- Python 3.8 or higher.

### Clone the Repository

```
git clone https://github.com/nanya01/web_crawler_apache_camel_issues_reports
.git
```

Create a Virtual Environment (Recommended)
```
python -m venv venv

source venv/bin/activate  # For macOS/Linux

venv\Scripts\activate     # For Windows
```

Install all dependencies using:

```
pip install -r requirements.txt
```

---

## Usages
Use the command-line to run the program
```
python main.py
```

Output Example

CSV File: apache_camel_issues.csv

---

## Challenges And Workarounds in Extracting Apache Camel Issues

1️ Issue Extraction Failure

Problem: Unable to successfully extract Apache Camel issues IDs directly from Jira.

Workaround:
- Identified that issue IDs generally follow a sequential pattern, with a few exceptions.
- Dynamically generated issue IDs based on this pattern to populate camel-id, allowing for more efficient retrieval of issues.

2️ Unable to Extract Comments

Problem: Could not successfully retrieve comments associated with issues.

Workaround:
- No effective workaround was found.

