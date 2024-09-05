-  In this level all we need to do is to clone a git repository and read the password inside it
- We clone the repository using the command: ```git clone ssh://bandit30-git@localhost:2220/home/bandit30-git/repo```
- The password for the repository is same as the password for the ```bandit30``` user
- We then navigate inside the repo
- There is a ```README.md``` file that doesn't have anything useful
- However, if we poke around, there is a git tag named ```secret```
- We show the details of the tag using the command ```git show secret```
- The ```secret``` has the password

Obtained password: fb5S2xb7bRyFmAvQYQGEqsbhVyJqhnDy