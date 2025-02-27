import requests
from bs4 import BeautifulSoup
import datetime

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

    
    # Extract Created Date & Convert to Epoch
    created_date, created_epoch = extract_date(soup, 'created-val')

    # Extract Updated Date
    updated_date, _ = extract_date(soup, 'updated-val')

    # Extract Resolution Date
    resolution_date, _ = extract_date(soup, 'resolutiondate-val')
    
     # Extract Description (Focusing on the <p> tag inside "user-content-block")
    desc_element = soup.find('div', {'id': 'description-val'})
    user_content = desc_element.find('div', {'class': 'user-content-block'}) if desc_element else None
    p_tag = user_content.find('p') if user_content else None
    description = p_tag.text.strip()
    print(f"Desc {description}")


def extract_date(soup, element_id):
    # Extract date from a given element and convert to epoch format.
    element = soup.find('span', {'id': element_id})
    time_tag = element.find('time') if element else None
    date_str = time_tag['datetime'] if time_tag and 'datetime' in time_tag.attrs else ''
    
    if date_str:
        try:
            epoch_time = int(datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z").timestamp())
        except ValueError:
            epoch_time = ''
    else:
        epoch_time = ''
    
    return date_str, epoch_time

if __name__ == "__main__":
    issue_url = "https://issues.apache.org/jira/browse/CAMEL-10597"
    fetch_issues(issue_url)