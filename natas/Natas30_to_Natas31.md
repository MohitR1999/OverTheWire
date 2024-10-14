- This level again deals with SQL injection, but this time in Perl
- Fortunately this time we are able to access the source code, so let's have a look at the major area of interest in it
```perl
if ('POST' eq request_method && param('username') && param('password')){
    my $dbh = DBI->connect( "DBI:mysql:natas30","natas30", "<censored>", {'RaiseError' => 1});
    my $query="Select * FROM users where username =".$dbh->quote(param('username')) . " and password =".$dbh->quote(param('password')); 
    my $sth = $dbh->prepare($query);
    $sth->execute();
    my $ver = $sth->fetch();
    if ($ver){
        print "win!<br>";
        print "here is your result:<br>";
        print @$ver;
    }
    else{
        print "fail :(";
    }
    $sth->finish();
    $dbh->disconnect();
}
```
- We can see that the method `quote` is directly invoked with the query params `username` and `password`, so these are the fields which we can control directly. However this `quote` method escapes the quotes, so it hinders us from running our malicious SQL query
- However, the `quote` method is context-sensitive, and it applies the escaping mechanism only if the argument passed to it is a string. In case there are multiple arguments passed, it will escape the first argument according to the second one
- In Perl, this `quote` method does not escape the first argument passed to it if the second argument passed defines the type of the first one as an integer, hence that could be used
- Also, if the `quote` method receives a list of arguments, it would treat them as separate arguments, which means if we provide two `username`s or `password`s in our request, they can be used to control the escaping
- Therefore, we craft the following payload:
```
username=natas31&password='lol' or 1=1&password=4
```
- This payload supplies one value for `username` and two values for `password`, wherein the first value of `password` is our query which we want to execute, and the second value is the definition of the data type that is being escaped. `4` stands for `SQL_INTEGER` type, hence Perl treats it as an integer and does not do any escaping, thereby firing our query
- This gives us the password for the next level: m7bfjAHpJmSYgQWWeqRE2qVBuMiRNq0y