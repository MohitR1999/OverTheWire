- This challenge presents us with a form that will search our query in a list of words, from the file ```dictionary.txt```
- Upon going through the mimic source code that is provided in the page, we find the following PHP code:
```php
<?
$key = "";
	if(array_key_exists("needle", $_REQUEST)) {
		$key = $_REQUEST["needle"];
	}
	if($key != "") {
		passthru("grep -i $key dictionary.txt");
	}
?>
```
- There's a parameter ```key``` that is present in the form data which goes to the server side on submitting, and if it is not empty, then it is passed straight into the ```passthru``` method that executes the linux ```grep``` command with it
- The method ```passthru``` in PHP allows us to execute arbitrary code on the server side. However, we can clearly see that the input is not sanitised well, which would also allow us to run arbitrary commands, even those which might not be justified in the context of the web application
- So, as the input is not sanitised in any way, we drop the following payload in the application: ```-e ".*" /etc/natas_webpass/natas10```
- The breakdown of this payload is as follows:
	- Since our ```key``` would be passed inside the ```grep``` command, we can try to read the file ```/etc/natas_webpass/natas10``` as it would contain the password
	- How to read a file using ```grep```? Well, the primary function of ```grep``` is to read a file AND find the strings that match a specific regular expression. So what if we pass a regular expression that can match everything? That would satisfy our purpose of reading the file
	- The ```-e``` flag in grep allows us to use any regular expression as the input, so we specify ```".*"```, which will match everything
	- And then finally we pass in the file name which we want to read, in our case it is ```/etc/natas_webpass/natas10```
	- So essentially, our ```grep``` command becomes like this: ```grep -i -e ".*" /etc/natas_webpass/natas10 dictionary.txt```
- Upon running the search with the above payload, we get a huge list of results, the first one being the password present inside ```/etc/natas_webpass/natas10```, and then the contents of ```dictionary.txt```, as it also served as a file parameter to ```grep```. However, we achieved what we were looking out for. The password is found :)
- Obtained password for ```natas10```: t7I5VHvpa14sJTUGV0cbEsbYfFP2dmOu