import urllib.parse
import requests
from requests.auth import HTTPBasicAuth
import base64
import string

URL = "http://natas28.natas.labs.overthewire.org"
auth_header = HTTPBasicAuth('natas28', '1JNwQM1Oi6J6j1k49Xyw7ZN6pXMQInVj')
initial_request_url = f"{URL}/index.php"
charset = string.ascii_lowercase

for letter in charset:
    initial_request_body = { 'query' : letter }
    r = requests.post(initial_request_url, auth=auth_header, data=initial_request_body, allow_redirects=False)
    response = urllib.parse.unquote(r.headers['Location']).split('?query=')[1]
    hex_response = base64.b64decode(response).hex()
    print(f"Character {letter}: {hex_response}, length: {len(hex_response)}")