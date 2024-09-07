- This page also presents us with some PHP related challenge, specifics of which I don't know
- Upon inspecting the page's source, I come across an interesting comment: ``` hint: password for webuser natas8 is in /etc/natas_webpass/natas8 ```
- This means we somehow need to read this file via the browser
- Fiddling around with the query params in the URL, I tried checking if there is some XSS present on the webpage (might be an absurd idea for an experienced hacker), so I just used the old classic XSS payload: ```<script>alert(1);</script>``` for the ```page``` query param
- However, instead of getting any popup, I encountered an error stating as follows:
```
Warning: include(<script>alert(1);</script>): failed to open stream: No such file or directory in /var/www/natas/natas7/index.php on line 21  
  
Warning: include(): Failed opening '<script>alert(1);</script>' for inclusion (include_path='.:/usr/share/php') in /var/www/natas/natas7/index.php on line 21
```
- The error message clearly stated that whatever we pass in the URL, it tried to include that
- So, on the lines of the hint that I had got earlier, I tried passing the parameter ```/etc/natas_webpass/natas8```
- And, as expected, it showed the password for the next level, ```natas8```. Unsafe PHP ftw!
- Obtained password: xcoXLmzMkoIP9D7hlgPlh9XD7OgLAe5Q
