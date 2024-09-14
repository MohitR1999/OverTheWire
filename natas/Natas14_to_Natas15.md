- This is the first level that requires some knowledge of SQL Injection
- We are presented with a form that accepts username and password
- We go through the mimic source code of the page and find that if we provide a successful query that can list all the users, then we will be presented with the password
- So we craft a payload to present in the ```username``` parameter, which is:
```SQL
" or 1=1; -- 
```
- Structure of the payload:
	- The first double quote ends the ```username``` string prematurely, paving way for our SQL code to be executed
	- We present a truthful condition with an ```OR``` operator, thereby resulting the expression to always return true
	- Finally we append the ```--``` to comment out rest of the code. Point to be noted here is the ```--``` is followed by a space
- We run this query, and in order to debug our query we set the ```debug``` query parameter to true. In order to have better access to the request, we can use burpsuite.
- Obtained password: SdqIqBsFcz3yotlNYErZSZwblkm0lrvx 