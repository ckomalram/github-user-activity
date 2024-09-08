from datetime import timedelta, datetime
import os
import sys
import http.client
import json

CACHE_EXPIRATION_TIME = timedelta(minutes=10)
CACHE_DIR = "users_cache"

def save_cache(username, data):
    cache_file = (f"{CACHE_DIR}/.cache_{username}.json")
    with open(cache_file, 'w') as file:
        json.dump({"timestamp": datetime.now().isoformat(), "data": data}, file)

def load_from_cache(username):
    cache_file = f"{CACHE_DIR}/.cache_{username}.json"
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as file:
            cached_data = json.load(file)
            cache_time = datetime.fromisoformat(cached_data["timestamp"])
            if datetime.now() - cache_time < CACHE_EXPIRATION_TIME:
                return cached_data["data"]
            else:
                print("Cache expired.")
    return None
     
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
        elif event_type == "ForkEvent":
            print(f"- Forked {repo_name}")
        elif event_type == "CreateEvent":
            ref_type = event.get("payload", {}).get("ref_type")
            ref_name = event.get("payload", {}).get("ref")
            print(f"- Created {ref_type} {ref_name} in {repo_name}")
        elif event_type == "DeleteEvent":
            ref_type = event.get("payload", {}).get("ref_type")
            ref_name = event.get("payload", {}).get("ref")
            print(f"- Deleted {ref_type} {ref_name} from {repo_name}")
        else:
            print(f"- {event_type} in {repo_name}")

def decode_response(data):
        try:
            events = json.loads(data)
            return events
        except json.JSONDecodeError:
            print(f"Failed to parse the response from GITHUB API")
            return []         

# https://api.github.com/users/ckomalram/events
def execute_api(username):

    cached_data = load_from_cache(username)
    if cached_data:
        print("Using cached data...")
        return cached_data

    conn = http.client.HTTPSConnection("api.github.com")
    endpoint = f"/users/{username}/events"
    github_token = os.getenv("GITHUB_TOKEN") #change every 30 days from github account

    if not github_token:
        print("Error: GITHUB_TOKEN not defined. Please, configure it, on env.")
        return [] 
    headers = {
        "User-Agent": "PythonScript",  # GitHub requiere un User-Agent personalizado
        "Authorization": f"token {github_token}"
    }

    try:
        conn.request("GET", endpoint, headers=headers)
        res = conn.getresponse()
        data = res.read()

        if res.status == 404:
            print(f"User '{username}' not found. Please check the username.")
            return []
        elif res.status == 403:
            print("Rate limit exceeded or access forbidden. Please try again later.")
            return []
        elif res.status != 200:
            print(f"Failed to fetch activity for user {username}. Status Code => {res.status}")
            return []    

        events = decode_response(data)    
        save_cache(username, events)

    except http.client.HTTPException as http_error:
        print(f"An Http Error ocurred: {http_error}")
        return []
    except Exception as err:
        print(f"An error ocurred: {err}")
        return []
    finally:
        conn.close() 
    
    return events

def run():
    if len(sys.argv) < 2:
        print("Usage: python3 github_activity.py <username>")
        return
    
    username = sys.argv[1]
    event_type = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"Fetching activity for github user: {username}")
    events = execute_api(username)
    if event_type:
        events = [event for event in events if event.get("type") == event_type]
        print(f"Filtered events by type: {event_type}")
    
    display_events(events)


if __name__ == "__main__":
    run()