- This level really starts getting into our PHP skills, fortunately I have google to the rescue ;)
- So on this level, we have a form that takes in a secret and compares it to the secret value that we already have on the server. If these values match, we will get our password
- How do I know this? Well, the same strategy of putting in a mimic of the page's source is also available on this leve
- Upon viewing the mimic source, I found the following PHP code:
```php
$encodedSecret = "3d3d516343746d4d6d6c315669563362";      function encodeSecret($secret) {       return bin2hex(strrev(base64_encode($secret)));
}      
if(array_key_exists("submit", $_POST)) {
	if(encodeSecret($_POST['secret']) == $encodedSecret) {
		print "Access granted. The password for natas9 is <censored>";} 
	else {
		print "Wrong secret";
	}
}
```
- Going through the code, I find that the code calls the function ```encodeSecret``` modifies the input secret so that it matches the ```encodedSecret``` variable's value
- Inside the ```encodeSecret``` function, I observed that it first called the method ```bin2hex```. Going through the PHP docs for ```bin2hex```, which are available [here](https://www.php.net/manual/en/function.bin2hex.php), I found that this method just converts binary data into hexadecimal. There's also a method called ```hex2bin```, which does the opposite
- So in this case, I fired up an online PHP shell, in which I called this ```hex2bin``` method, and passed this value of ```encodedSecret``` variable. The output was ```==QcCtmMml1ViV3b```
- This seemed like a reversed base64 encoded string, which was apparent from the function definition as it reverses the string which has been base64 encoded first
- So we go to our good old reliable tool, [Cyberchef](https://gchq.github.io/CyberChef/). We bake a recipe to first REVERSE the input string, character by character, and then DECODE from base64. Applying this operation, we get ```oubWYf2kBq```
- We pass this obtained value in the form, and boom! Our level is cleared and we get the password for new level. Finally
- Obtained password for ```natas9```: ZE1ck82lmdGIoErlhQgWND6j2Wzz6b6t