import os
import sys
import http.client
import json

# https://api.github.com/users/ckomalram/events
def execute_api(username):
    conn = http.client.HTTPSConnection("api.github.com")
    endpoint = f"/users/{username}/events"
    github_token = os.getenv("GITHUB_TOKEN") #change every 30 days from github account
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
    print(events)

# TODO Recorrer los eventos y mostrar resumen

def run():
    if len(sys.argv) < 2:
        print("Usage: python3 github_activity.py <username>")
        return
    username = sys.argv[1]
    print(f"Fetching activity for github user: {username}")
    execute_api(username)


if __name__ == "__main__":
    run()