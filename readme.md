# Github User Activity
In this project, you will build a simple command line interface (CLI) to fetch the recent activity of a GitHub user and display it in the terminal. This project will help you practice your programming skills, including working with APIs, handling JSON data, and building a simple CLI application.

## Requirements:
- Python 3.x

## Installation:
    ```sh   
    git clone
    python3 -m venv env    
    source env/bin/activate
    cd github-user-activity
    pip3 install -r requirements.txt
    ``` 
## Token
You should go to your github account and create a classic repo token.
- Use that in a VAR inside of activate File of your env folder (env/bin/activate).
    ```sh  
    export GITHUB_TOKEN='put_ur_token_'
    ``` 
[Example of stackoverflow](https://stackoverflow.com/questions/39056356/how-can-i-use-a-postactivate-script-using-python-3-venv)

## Commands - CLI
### List all events
    ```sh  
    python3 github_activity.py <username>
    ```

### Filter By event type
    ```sh  
    python3 github_activity.py <username> [CreateEvent|PushEvent|ForkEvent|IssuesEvent|WatchEvent|DeleteEvent]
    ```

## Project url
- [github-activity](https://roadmap.sh/projects/github-user-activity)
- [replit-github-activity](https://replit.com/@glaw14/github-user-activity)

## Contributing
If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (git checkout -b feature/new-feature).
3. Make your changes and commit them (git commit -am 'Add new feature').
4. Push the branch to your fork (git push origin feature/new-feature).
5. Open a new Pull Request.


## License
This project is licensed under the MIT License.