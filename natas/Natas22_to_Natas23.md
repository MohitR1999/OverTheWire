- You probably don't even need to read this writeup if you've solved till now. This is easier than anything else till now
- All we need is to append the `revelio` query parameter in our request and it will reveal the password
- Boom! It DID NOT work in the browser haha
- Actually the response header is setting the `Location` attribute to `/`, the root of the website, so we can't possibly do this in the browser
- But we can do the same in Burpsuite, by intercepting and repeating the request.
- I guess this level cannot be solved without Burp, so it would be better to have it up and running now if not done before
- Obtained password: dIUQcI3uSus1JEOSSWRAEXBG8KbR8tRs