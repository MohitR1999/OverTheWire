- We login to a weird shell where everything is in uppercase
- No command is being permitted, and we get a permission denied error
- However, since we know that the default shell for the user is set in the environment variable ```$0```, we just simply execute it
- We have a ```sh``` shell now. Using this, we simply read the password for ```bandit33``` that is present inside ```/etc/bandit_pass/bandit33```
- Obtained password: tQdtbs5D5i2vJwkO8mEyYEyTL8izoeJ0