#!/usr/bin/env python3
import sys
import json
import urllib.request
import urllib.error

def fetch_github_activity(username):
    url=f"https://api.github.com/users/{username}/events"
    
    try:
        with urllib.request.urlopen(url) as response:
            if response.status !=200:
                print(f"Error: Ne udalos poluchit dannie (HTTP {response.status})")
                return
            data=response.read()
            events=json.loads(data)
            
            if not events:
                print("Net nedavnyh activenosti")
                return
            for event in events:
                event_type=event.get("type", "")
                repo_name=event.get("repo", {}.get("name", "") )
                
                if event_type=="PushEvent":
                    commits=len(event.get("payload", {}).get("commits", []))
                    print (f"Pushed {commits} commit(s) {repo_name}")
                elif event_type=="IssuesEvent":
                    action=event.get("payload", {}).get("action", "")
                    print(f"{action.capitalize()} an issue in {repo_name}")
                elif event_type=="PullRequestEvent":
                    action=event.get("payload", {}).get("action", "")
                    print(f"{action.capitalize()} a pull request in {repo_name}")
                elif event_type=="WatchEvent":
                    print(f"Starred {repo_name}")
                else:
                    print(f"{event_type} on {repo_name}")
                    
    except urllib.error.HTTPError as e:
        if e.code==404:
            print("Polzovatel ne naiden")
        else:
            print(f"HTTP oshipka: {e.code}")
    except urllib.error.URLError as e:
        print(f"Oshibka soedenenie: {e.reason}")
    except json.JSONDecodeError:
        print("Oshibka obrabotki dannyh JSON")
        
def main():
    if len(sys.argv) !=2:
        print("Ispolzovanie: github-activity <username>")
        return
    
    username=sys.argv[1]
    fetch_github_activity(username)
    
if __name__=="__main__":
    main()
                    