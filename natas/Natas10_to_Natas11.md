- This level is very similar to the level ```natas9```, except for one fact: Now there is a certain level of input sanitization before it is being passed to the ```passthru``` function call
- Upon going through the mimic source code of the page, we find the following PHP code:
```php
<?
$key = "";
if(array_key_exists("needle", $_REQUEST)) {
	$key = $_REQUEST["needle"];
}
if($key != "") {
	if(preg_match('/[;|&]/',$key)){
		print "Input contains an illegal character!";
	} else {
		passthru("grep -i $key dictionary.txt");
	}
}
?>
```
- Here we see that the input is tested against a regular expression of ```[;|&]```, and if it matches, the ```passthru``` function will not be called. So somehow we need to escape the regular expression match
- The test considers the characters that could be used to run multiple linux commands on the same line consecutively. So it implies that it would be very difficult for us to run another command by terminating ```grep``` preemptively
- However, if we think carefully, we can try the same payload that we used to solve the level ```natas9```, because none of the characters that we used in that payload would be restricted in this level
- So we modify the payload accordingly to this value: ```-e ".*" /etc/natas_webpass/natas11```
- Upon running the query, we get the same result as before, solving the level and obtaining the password for user ```natas11```
- Obtained password: UJdqkK1pTu6VLt9UHWAgRZz6sVUZ3lEk