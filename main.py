

import requests
import json

# Github Personal access token
TOKEN = "YOUR PAT TOKEN"

# Github repository owner and repository name
OWNER = "YOURUSERNAME"
REPO = "REPO NAME"


def delete_old_releases(check_versions: bool = True):
    # Get all releases for the repository
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/releases"
    headers = {"Authorization": f"Token {TOKEN}"}
    response = requests.get(url, headers=headers)

    # Parse response to get a list of releases
    releases = json.loads(response.text)

    # Loop through releases
    for release in releases:
        # Get version of the release
        version = release["tag_name"]
        # Split version by '.'
        version_parts = version.replace("v", "").split(".")
        # Check if version is less than v1.0
        try:
            if int(version_parts[0]) < 1:
                # Delete the release
            
                if not check_versions:
                    delete_release = release["url"]
                    requests.delete(delete_release, headers=headers)

                    delete_tag = f"https://api.github.com/repos/{OWNER}/{REPO}/git/refs/tags/{version}"
                    requests.delete(delete_tag, headers=headers)
                    print(f"Deleted release {version}")
                else:
                    print("Version release " + version)
        except:
            pass


def delete_old_actions(version_name = "build", check_versions=True):
    # Get all workflows for the repository
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows"
    headers = {"Authorization": f"Token {TOKEN}"}
    response = requests.get(url, headers=headers)

    # Parse response to get a list of workflows
    workflows = json.loads(response.text)

    # Loop through workflows
    for workflow in workflows["workflows"]:
        # Get the runs of the workflow
        runs_url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{workflow['id']}/runs"
        runs_response = requests.get(runs_url, headers=headers)
        runs = json.loads(runs_response.text)
        # Loop through runs
        for run in runs["workflow_runs"]:
            # Get the name of the run
            name = run["display_title"]
            if name == version_name:
                # Delete the run
                if not check_versions:
                    delete_url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs/{run['id']}"
                    requests.delete(delete_url, headers=headers)
                   # check = input("Are you sure you want to delete this run? (y/n/ALL)")
                   # if check == "y":
                   #     print(f"Deleted run {name}")
                    print(f"Deleted run {name}")
            
            elif check_versions:
                print("Version run " + name)


## Using Check_Versions does not allow it to delete anything.

delete_old_actions(version_name = "build", check_versions=True)
delete_old_releases(check_versions=True)
