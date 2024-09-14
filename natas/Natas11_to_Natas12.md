- This level tests our cryptography skills, especially the one involving breaking a cipher algorithm
- So the mimic code in this case looks like this:
```php
<?
$defaultdata = array( "showpassword"=>"no", "bgcolor"=>"#ffffff");
function xor_encrypt($in) {
	$key = '<censored>';
	$text = $in;
	$outText = '';
	// Iterate through each character
	for($i=0;$i<strlen($text);$i++) {
		$outText .= $text[$i] ^ $key[$i % strlen($key)];
	}
	return $outText;
}

function loadData($def) {
	global $_COOKIE;
	$mydata = $def;
	if(array_key_exists("data", $_COOKIE)) {
	$tempdata = json_decode(xor_encrypt(base64_decode($_COOKIE["data"])), true);
	if(is_array($tempdata) && array_key_exists("showpassword", $tempdata) && array_key_exists("bgcolor", $tempdata)) {
			if (preg_match('/^#(?:[a-f\d]{6})$/i', $tempdata['bgcolor'])) {
				$mydata['showpassword'] = $tempdata['showpassword'];
				$mydata['bgcolor'] = $tempdata['bgcolor'];
			}
		}
	}
	return $mydata;
}

function saveData($d) {
	setcookie("data", base64_encode(xor_encrypt(json_encode($d))));
}

$data = loadData($defaultdata);

if(array_key_exists("bgcolor",$_REQUEST)) {
	if (preg_match('/^#(?:[a-f\d]{6})$/i', $_REQUEST['bgcolor'])) {
		$data['bgcolor'] = $_REQUEST['bgcolor'];
	}
}
saveData($data);
?>
```
- Going through the script, I realised that the function ```xor_encrypt``` is the crux of the problem which we need to tackle, as the other functions are taking care of the rest of stuff
- I also realised that the cookie contained two keys, ```showpassword``` and ```bgcolor```, out of which if we somehow set the value of ```showpassword``` to ```yes```, then we can get the password to the next level
- So shifting our focus to ```xor_encrypt```, I observed that it does a character by character XOR of the plaintext with the key, that is unknown to us. However, using the properties of XOR cipher, we can try to find the key
- XOR has the following properties:
	- plaintext XOR key = ciphertext
	- ciphertext XOR key = plaintext
	- ciphertext XOR plaintext = key
- So in order to modify the cookie, we need to first find the key, then place the XOR encrypted cookie in its place
- Going through the code, we can observe that initially the value of ```showpassword``` is set to ```no``` and ```bgcolor``` is set to ```#ffffff```
- This array is first JSON encoded, then XOR encrypted, then base64 encoded, and then stored in the browser's storage in URL encoded format (the ```setcookie``` method in PHP URL encodes the cookie)
- So we can take the function ```xor_encrypt```, and in place of ```key``` we can use the JSON encoded plaintext consisting of these two variables, ```showpassword``` and ```bgcolor```, along with the encrypted cookie and try to decode it using the following code:
```php
<?php
$cookie = "HmYkBwozJw4WNyAAFyB1VUcqOE1JZjUIBis7ABdmbU1GIjEJAyIxTRg%3D";
$cookie = urldecode($cookie);
$cookie = base64_decode($cookie);
function xor_encrypt($in) {
	$key = json_encode(array("showpassword" => "no", "bgcolor" => "#ffffff"));
	$text = $in;
	$outText = '';
	// Iterate through each character
	for ($i = 0; $i < strlen($text); $i++) {
		$outText .= $text[$i] ^ $key[$i % strlen($key)];
	}
	return $outText;
}
echo xor_encrypt($cookie);
?>
```
- The code does the following:
	- First we store the cookie that was set in the browser, as it is
	- We first URL decode it, then base64 decode it
	- So we have the raw XOR encrypted ciphertext with us
	- We now JSON encode the default data array in the ```xor_encrypt``` function, that will act as the plaintext
	- Hence, we have our ciphertext and plaintext both, so we can XOR them and get the key
	- Upon running this PHP code, we get the following output: ```eDWoeDWoeDWoeDWoeDWoeDWoeDWoeDWoeDWoeDWoe```
	- It is a repeating key XOR cipher, with the key as ```eDWo```
- So now we have the key, we can use it to encrypt our modified cookie and set it in the browser
- I then used the following code to get the cookie:
```php
function xor_encrypt($in)
{
	$key = 'eDWo';
	$text = $in;
	$outText = '';
	// Iterate through each character
	for ($i = 0; $i < strlen($text); $i++) {
		$outText .= $text[$i] ^ $key[$i % strlen($key)];
	}
	return $outText;
}
$new_cookie_array = array("showpassword" => "yes", "bgcolor" => "#f0f0aa");
echo base64_encode(xor_encrypt(json_encode($new_cookie_array)));
```
- The code, now equipped with the key, can encrypt our new cookie as well, inside which we set the value of ```showpassword``` to ```yes```
- We then JSON encode it, XOR encrypt it, and base64 encode it and set it in the browser using the following command: ```document.cookie="the_new_cookie";```
- Once we set the cookie and refresh the page, the password appears on the page as expected :)
- Obtained password for the next level: yZdkjAYZRd3R7tq7T5kXMjMJlOIkzDeB