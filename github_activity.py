import os
import sys
import http.client
import json

# https://api.github.com/users/ckomalram/events
def execute_api(username):
    conn = http.client.HTTPSConnection("api.github.com")
    endpoint = f"/users/{username}/events"
    github_token = os.getenv("GITHUB_TOKEN") #change every 30 days from github account
    if not github_token:
        print("Error: GITHUB_TOKEN not defined. Please, configure it, on env.")
        return
    headers = {
        "User-Agent": "PythonScript",  # GitHub requiere un User-Agent personalizado
        "Authorization": f"token {github_token}"
    }
    conn.request("GET", endpoint, headers=headers)
    res = conn.getresponse()
    data = res.read()
    

    if res.status != 200:
        print(f"Failed to fetch activity for user {username}. Status Code => {res.status}")
        return
    events = json.loads(data)
    #print(events)
    display_events(events)

# TODO Recorrer los eventos y mostrar resumen
def display_events(events):
    if not events:
        print("No recent events found for this user.")
    
    for event in events:
        event_type = event.get("type")
        repo_name = event.get("repo", {}).get("name")
        if event_type == "PushEvent":
            commit_count = len(event.get("payload", {}).get("commits", []))
            print(f"- Pushed {commit_count} commit(s) to {repo_name}")
        elif event_type == "IssuesEvent":
            action = event.get("payload", {}).get("action")
            print(f"- {action.capitalize()} an issue in {repo_name}")
        elif event_type == "WatchEvent":
            print(f"- Starred {repo_name}")
        # Agregar más tipos de eventos según sea necesario
        else:
            print(f"- {event_type} in {repo_name}")
        #print(f"Event Type => {event_type} -- Repo Name => {repo_name}")


def run():
    if len(sys.argv) < 2:
        print("Usage: python3 github_activity.py <username>")
        return
    username = sys.argv[1]
    print(f"Fetching activity for github user: {username}")
    execute_api(username)


if __name__ == "__main__":
    run()