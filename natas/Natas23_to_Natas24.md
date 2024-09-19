- This level is a play on PHP internals
- We have the following source code mimic:
```php
<?php
if(array_key_exists("passwd",$_REQUEST)){
	if(strstr($_REQUEST["passwd"],"iloveyou") && ($_REQUEST["passwd"] > 10 )){
		echo "<br>The credentials for the next level are:<br>";
		echo "<pre>Username: natas24 Password: <censored></pre>";
	}
	else{
		echo "<br>Wrong!<br>";
	}
}
// morla / 10111
?>
```
- Now this looks pretty simple, all we need to do is to just pass the word `iloveyou` in the query params for parameter `passwd`, however the second condition that checks the string against the number `10` poses a problem
- But, in PHP, if there's a number in the beginning of a string, then during implicit conversion the string following the number is removed and all we are left is the number at the beginning
- So, we can pass the word `11iloveyou`, as it will pass the check of `strstr()` function and will also the comparison check
- We submit the form with this value, and obtain the password: MeuqmfJ8DDKuTr5pcvzFKSwlxedZYEWd