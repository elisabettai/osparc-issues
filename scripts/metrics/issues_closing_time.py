"""
In order to use these scripts one needs to:
- get a Personal Access Token on github: https://github.com/settings/tokens?type=beta
  - Resource owner must be ITISFoundation
  - Repository access must be: All repositories
  - Permissions on repositories: Issues ReadWrite

"""

import getpass
from datetime import datetime
from http import HTTPStatus

import requests

# Set up your personal access token
token = getpass.getpass("Enter your personal access token:")

# Set the repository details
owner = "ITISFoundation"
repo = "osparc-issues"

# Prompt for the start date
start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")


# Make the API request to retrieve the closed issues
url = f"https://api.github.com/repos/ITISFoundation/osparc-issues/issues"
params = {"state": "closed", "since": start_date, "until": end_date, "per_page": 40}
headers = {"Authorization": f"Bearer {token}"}

response = requests.get(url, params=params, headers=headers)
if response.status_code != HTTPStatus.OK:
    raise RuntimeError(
        f"Could not list issues, {response.reason} with {response.json()}"
    )
resp_json = response.json()

# # Fetch all closed issues by handling pagination
# while 'next' in response.links.keys():
#     response = requests.get(response.links['next']['url'], params=params, headers=headers)
#     resp_json.extend(response.json())

issues = resp_json

# Calculate the average time between start_date and closed_at
total_time = 0
num_issues = len(issues)

for issue in issues:
    closed_at = datetime.strptime(issue["closed_at"], "%Y-%m-%dT%H:%M:%SZ")
    start_date = datetime.strptime(issue["created_at"], "%Y-%m-%dT%H:%M:%SZ")
    time_diff = closed_at - start_date
    total_time += time_diff.total_seconds() / (60 * 60 * 24)

average_time = total_time / num_issues

# Display the average time
print(
    f"Average time to close issues: {average_time:.2f} days. This takes into account {num_issues} closed issues between {start_date} and {end_date}. WARNING: if you expect more than 100 issues, this scripts need to implement pagination"
)
