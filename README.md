MinIRC, a mini IRC-like tool

## Bug hunting

### Log in without the correct password

"login guest notguest" returns bad user or password but we are logged in anyway\
Security impact: high, we can login without password\
Test to verify: login guest notguest | whoami, if whoami returns that we are not logged in, we are ok
