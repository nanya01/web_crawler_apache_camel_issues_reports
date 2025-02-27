import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv

def fetch_issues(issues_url):
    response = requests.get(issues_url)
    if response.status_code != 200:
        print(f"Failed to fetch issues: {issues_url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    issue_details = {}
    # Extract Type
    type = soup.find('span', {'id': 'type-val'})
    issue_details['Type'] = type.text.strip() if type else 'Unknown'
    print(f"Type {type.text.strip()}")

    # Extract Assignee
    assignee = soup.find('span', {'id': 'assignee-val'})
    issue_details['Assignee'] = assignee.text.strip() if assignee else 'Unassigned'
    print(f"Assignee {assignee.text.strip()}")

    # Extract Reporter
    reporter = soup.find('span', {'id': 'reporter-val'})
    issue_details['Reporter'] = reporter.text.strip() if reporter else 'Unknown'
    print(f"Reporter {reporter.text.strip()}")

    # Extract Affected Versions
    affected_versions = soup.find('span', {'id': 'versions-val'})
    issue_details['Affected Versions'] = affected_versions.text.strip() if affected_versions else 'None'
    print(f"Affected versions {affected_versions.text.strip()}")

    # Extract Fix Versions
    fix_versions_element = soup.find('span', {'id': 'fixfor-val'})
    fix_versions_split = fix_versions_element.text.split()
    fix_versions = "".join(fix_versions_split)
    issue_details['Fix Versions'] = fix_versions if fix_versions else 'None'
    print(f"Fix Versions {fix_versions}")

    
     # Extract Created Date & Convert to Epoch
    created_date, created_epoch = extract_date(soup, 'created-val')
    issue_details['Created Date'] = created_date
    issue_details['Created Epoch'] = created_epoch

    # Extract Updated Date
    updated_date, _ = extract_date(soup, 'updated-val')
    issue_details['Updated Date'] = updated_date

    # Extract Resolution Date
    resolution_date, _ = extract_date(soup, 'resolutiondate-val')
    issue_details['Resolution Date'] = resolution_date
    
     # Extract Description (Focusing on the <p> tag inside "user-content-block")
    desc_element = soup.find('div', {'id': 'description-val'})
    user_content = desc_element.find('div', {'class': 'user-content-block'}) if desc_element else None
    p_tag = user_content.find('p') if user_content else None
    description = p_tag.text.strip()
    issue_details['Description'] = description if description else 'No description available'
    print(f"Desc {description}")

    return issue_details


def save_to_csv(issue_data, filename="apache_camel_issues.csv"):
    """Save issue data to a CSV file."""
    file_exists = False
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            file_exists = True
    except FileNotFoundError:
        pass

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=issue_data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(issue_data)

def extract_date(soup, element_id):
    # Extract date from a given element and convert to epoch format.
    element = soup.find('span', {'id': element_id})
    time_tag = element.find('time') if element else None
    date_str = time_tag['datetime'] if time_tag and 'datetime' in time_tag.attrs else ''
    
    if date_str:
        try:
            epoch_time = int(datetime.fromisoformat(date_str.replace('Z', '+00:00')).timestamp())
        except ValueError:
            epoch_time = ''
    else:
        epoch_time = ''
    
    return date_str, epoch_time

if __name__ == "__main__":
    issue_url = "https://issues.apache.org/jira/browse/CAMEL-10597"
    issue_data = fetch_issues(issue_url)
    save_to_csv(issue_data)