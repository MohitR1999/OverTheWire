- This level is also a play on the PHP internals
- We have the following mimic source code:
```php
<?php
if(array_key_exists("passwd",$_REQUEST)){
	if(!strcmp($_REQUEST["passwd"],"<censored>")){
		echo "<br>The credentials for the next level are:<br>";
		echo "<pre>Username: natas25 Password: <censored></pre>";
	}
	else{
		echo "<br>Wrong!<br>";
	}
}
// morla / 10111
?>
```
- So the code compares the value of `$_REQUEST['passwd']` to the password of this level (which we don't know), and only then it reveals the password. Kinda illogical as if we had known the password already, then we would have completed the level as well
- However, a deeper look into the code reveals that we need to bypass the `strcmp()` function in PHP somehow
- Now this function compares two strings and returns `0` if both the strings are equal. However, if one of the parameters is not a string (like a `NULL`), then also it returns 0, which means it can be exploited that way
- So we can see that the `passwd` is a request query parameter which we can control. Passing any string for the `passwd` parameter results in the check getting failed and we end up in the `else` block
- So for our case, we somehow need to pass a non-string value to the `strcmp` function through the request query params. One way we can do it by sending the `passwd` param as an array instead of a string, like this: ```GET /?passwd[]=test HTTP/1.1```
- Sending the request with this query parameter results in the `strcmp()` method returning `0`, and hence we go through the check and the password is revealed
- Obtained password: ckELKUWZUfpOv6uxS6M7lXBpBssJZ4Ws