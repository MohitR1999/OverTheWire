- This level is a bit tricky as there is literally nothing in the page's source or network requests or request headers
- There was a small hint on the page: an image of size 1 pixel was being loaded from a relative URL, and that too without any authorisation, so I felt like there might be something on that relative path
- So after a bit of fiddling around, I observed that the ```files``` directory can be accessed on the domain ```natas2.natas.labs.overthewire.org``` without any authorisation
- So I hit the URL : ```http://natas2.natas.labs.overthewire.org/files/```
- There was a list of contents of the public directory that had a file named ```users.txt```
- Opening that file revealed the passwords
- Obtained password: 3gqisGdR0pjm6tpkDKdIWO2hSvchLeYH