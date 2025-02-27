import requests
from bs4 import BeautifulSoup

def fetch_issues(issues_url):
    response = requests.get(issues_url)
    if response.status_code != 200:
        print(f"Failed to fetch issues: {issues_url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract Type
    type = soup.find('span', {'id': 'type-val'})
    print(f"Type {type.text.strip()}")

    # Extract Assignee
    assignee = soup.find('span', {'id': 'assignee-val'})
    print(f"Assignee {assignee.text.strip()}")

    # Extract Reporter
    reporter = soup.find('span', {'id': 'reporter-val'})
    print(f"Reporter {reporter.text.strip()}")

    # Extract Affected Versions
    affected_versions = soup.find('span', {'id': 'versions-val'})
    print(f"Affected versions {affected_versions.text.strip()}")

    # Extract Fix Versions
    fix_versions_element = soup.find('span', {'id': 'fixfor-val'})
    fix_versions = fix_versions_element.text.split()
    print(f"Fix Versions {" ".join(fix_versions)}")

    

if __name__ == "__main__":
    issue_url = "https://issues.apache.org/jira/browse/CAMEL-10597"
    fetch_issues(issue_url)