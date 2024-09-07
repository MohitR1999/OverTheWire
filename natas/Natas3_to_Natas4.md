- This level also doesn't have any content on the page, as well as there is no content that is being loaded from an external URL
- So I thought about a possible URL that might be present on the website domain
- I thought about the file ```robots.txt```, that limits what a web crawler can index on that particular domain
- I accessed the file, and it had the following content:
```text
User-agent: *
Disallow: /s3cr3t/
```
- So naturally, I then tried hitting the URL mentioned in the ```Disallow``` parameter
- Upon hitting the URL: ```http://natas3.natas.labs.overthewire.org/s3cr3t/```, I found the directory listing that contained the file ```users.txt```, again
- This time it had the password for ```natas4```
- Obtained password: QryZXc2e0zahULdHrtHxzyYkj59kUxLQ