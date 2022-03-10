MinIRC, a mini IRC-like tool

## Bug hunting

### Log in without the correct password

"login guest notguest" returns bad user or password but we are logged in anyway\
Security impact: high, we can login without password\
Test to verify: login guest notguest | whoami, if whoami returns that we are not logged in, we are ok
Patched at commit a6ec342712389aa44fa4f727c18cb0612aa12910

### Added users are admin even if we specify that they are not

If you load users via a file, non-admin users will be admin in the server\
Security impact: high, added users are admin\
Test to verify: add a admin user and a non-admin user and see if they are both admin or not, only the admin should be admin\
Patched at commit 188b906e165699266c5cb7e5040d0c0851418769

