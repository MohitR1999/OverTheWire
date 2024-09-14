- For this level we will have to level up our skills and use a professional pentesting tool such as BurpSuite.
- This level requires us to upload a JPEG file to the server. However, there is no check on server side for which file is being uploaded
- Hence, we can upload any file, even a PHP file, and read the password of the next level user
- So for this purpose, we craft a simple PHP payload as follows:
```php
<?php echo passthru('cat /etc/natas_webpass/natas13'); ?>
```
- We simple upload this file and intercept the request in BurpSuite
- In the repeater, we modify the filename, just replace the ```.jpg``` extension with ```.php``` in the request body
- We fire the request, and as expected, it goes through and gives us a message with the randomly generated filename
- We click on the URL, our PHP payload is executed by the server, and it gives us the password for the next level
- Obtained password: trbs5pCjCrkuSknBBKHhaBxq6Wm1j3LC