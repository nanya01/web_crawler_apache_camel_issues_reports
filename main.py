import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By 
import time

def get_full_url(issue_id):
    base_url = "https://issues.apache.org/jira/browse/CAMEL-"
    return base_url + issue_id


def fetch_issues(issues_url):
    response = requests.get(issues_url)
    if response.status_code != 200:
        print(f"Failed to fetch issues: {issues_url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    issue_details = {}
    
    # Ensure Camel is the first header (for easy reference)
    issue_details['Camel Project ID'] = issue_url.split('-')[-1]  
    print(f"camel issue_url {issue_url.split('-')[-1] }")
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
    affected_versions_element = soup.find('span', {'id': 'versions-val'})
    affected_versions_split = affected_versions_element.text.split()
    affected_versions = "".join(affected_versions_split)
    issue_details['Affected Versions'] = affected_versions if affected_versions else 'None'
    print(f"Affected versions {affected_versions}")

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

    if user_content:
        p_tags = user_content.find_all('p')  
        description = "".join(p.text.strip() for p in p_tags if p.text.strip())  
    else:
        description = "No description available"

    issue_details['Description'] = description
    print(f"Description: {description}")


    # Extract Comments
    issue_details['Comments'] = extract_comments(issues_url)
    return issue_details


def save_to_csv(issue_data, filename="apache_camel_issues.csv"):
    """Save issue data to a CSV file."""
    file_exists = False
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            file_exists = True
    except FileNotFoundError:
        pass
    
    if isinstance(issue_data['Comments'], list):
        issue_data['Comments'] = repr(issue_data['Comments']) 

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

def extract_comments(issues_url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") 
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(issues_url)
        time.sleep(5) 

        comments = []
        comment_elements = driver.find_elements(By.CLASS_NAME, "activity-comment")

        for comment in comment_elements:
            try:
                author = comment.find_element(By.CLASS_NAME, "user-hover").text.strip()
            except:
                author = "Unknown"

            try:
                timestamp = comment.find_element(By.TAG_NAME, "time").get_attribute("datetime")
            except:
                timestamp = "No timestamp"

            try:
                comment_text = comment.find_element(By.CLASS_NAME, "action-body").text.strip()
            except:
                comment_text = "No comment text"

            comments.append(f"{author} - {timestamp} {comment_text}")

        full_comments = repr(comments) if comments else "No comments found"
        
        print(f"Extracted Comments: {full_comments}")  

        return full_comments

    except Exception as e:
        print(f"Error extracting comments: {e}")
        return "No comments found"

    finally:
        driver.quit()

if __name__ == "__main__":
    issue_ids = [str(id) for id in list(range(21847, 20814, -1)) + [10597]] 
    #issue_ids = input("Enter issue IDs (separated by commas): ").split(',')
    for issue_id in issue_ids:
        issue_id = issue_id.strip()  
        issue_url = get_full_url(issue_id)
        print(f"full issue url {issue_url}")
        issue_data = fetch_issues(issue_url)
        #print(f"issue data {issue_data}")
        if issue_data:
            save_to_csv(issue_data)
            print(f"Data saved for {issue_id}")
          