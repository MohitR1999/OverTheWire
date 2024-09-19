- This is the easiest level I came across so far in a while lmao
- In this level there are two websites, one present at the regular URL `http://natas21.natas.labs.overthewire.org/` and the other one 'co-located' at the URL `http://natas21-experimenter.natas.labs.overthewire.org/`
- The key point to be noted here is, co-located means these websites share some common server side PHP code, and this also means if we modify the `$_SESSION` superglobal on one, it would be changed and persisted across the other too
- So on the experimenter website we can see that there is a form that allows us to submit a few values
- We simply open up Burpsuite and intercept the request and send it to repeater (details in [[Natas20_to_Natas21|here]]), with the following contents of request body:
```text
align=right&fontsize=100%25&bgcolor=pink&submit=Update&admin=1
```
- After sending this request, we can see in the response that the values of these variables are set in the session
```text
[DEBUG] Session contents:<br>Array
(
    [debug] => 1
    [align] => right
    [fontsize] => 100%
    [bgcolor] => pink
    [submit] => Update
    [admin] => 1
)
```
- The value of `admin` is now set to `1`, so we now navigate to the original website, and use the same session ID that we sent in the request (In my case it was `jvpolkvjh4jilb34aa3jp0iavv`)
- Sending the request on the original one results in obtaining the password. Easy peasy :)
- Obtained password: d8rwGBl0Xslg3b76uh3fEbSlnOUBlozz