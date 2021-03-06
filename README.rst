Remote Runner
=============
Transfer a local script file to a remote host and execute it.


Requirements
============
- Python 2.7 and Python 3 are supported.
- Paramiko 1.10+.


Install
=======
::

    pip install remrunner


Synopsis
========
::

    from remrunner import runner
    r = runner.Runner(host, username)
    
    rval, stdout, stderr = r.run('/path/to/local/script.py')
    if rval:
        print(stderr)
    else:
        print(stdout)
 
    r.close()
  

Uses
====
- Great when using scripts to collect information from a large number of remote hosts. 
- No need to maintain scripts across multiple systems. Only the script versions on the local host need to be maintained.
  

Details
=======
Named files are copied to a temp location (./.remrunner/[PID]/) on the remote 
host, permissions are set to 0700, and script is then executed.

On cleanup, the [PID] directory and all contents are removed before closing
the connections.

 
API
===

Class Runner
------------

init(host, user, kwargs)
  *host* : Required. IP Address or FQDN
  
  *user* : Optional. Defaults to current running user on local machine.
  
  keyword-args:
  *auto_add* : (Boolean) Defaults to True. Set Paramiko Client.AutoAddPolicy.
  
  
run(script, sudo, timeout, opts)
  Run the named local script on remote host.
  
  *script* : Path to script on local machine
  
  *sudo* : (Boolean) Defaults to False. When true, the execution command on 
  remote machine will be prefaced with "sudo "
  
  *timeout* : (seconds, optional) Defaults to 10
  
  *opts* : optional command-line arguments that will be passed to remote script.
  

close()      
  Clean up temporary directories on remote host and close SSH and SFTP sessions.
  
 
Examples
========

- Run remote script with sudo::

    r.run(script, True)
    
- Run remote script and specify a 60 second timeout::

    r.run(script, False, 60)
     
- Run remote script with timeout and optional arguments::

    r.run(script, False, 15, "--verbose --interval=4")


Known Issues
============
Currently, as this is intended to be used for automation, *remrunner* assumes 
that SSH keys to allow password-less logins are already in place. 
There is no option to prompt for password or ssh passphrase. 
Maybe in a future release.


To Do
=====
Could use better exception handling in a few places.
Needs a tests.
Probably needs sanitizing/de-tainting of optional user arguments.

  
Author
======
Jeff Leary (sillymonkeysoftware -at- gmail -dot- com)

