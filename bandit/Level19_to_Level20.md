- This level requires us to use the ```setuid``` binary that is present in the home directory in order to change our privilege to the level of ```bandit20``` user and hence read the corresponding password
- For this we run the command: ```./bandit20-do cat /etc/bandit_pass/bandit20```
- The ```bandit20-do``` binary changes the user id in our case to the id of ```bandit20``` user and hence we are able to read the password file with the new permissions granted to us
- Obtained password: 0qXahG8ZjOVMN9Ghs7iOWsCfZyXOUbYO