from __future__ import unicode_literals
import os
import sys
import argparse
import paramiko
from remrunner import remotemanager

"""
Runs a local script on a remote host.
Local scripts are copied to the host and then executed.

Can be used as module, or standalone script.

Module example:

    from remrunner import runner
    r = runner.Runner(host, username)
    rval, out, err = r.run('/path/to/script.py', True, 30, "--interval=3 -v")
    r.close()
    
Script example:

    $> python remrunner.py --user=<user> --timeout=60 <host> <script>
    
    $> python remrunner.py --optargs="-v -ai" <host> <script>


Note:
Paramiko 1.10 or higher required. Previous version are buggy, prone
to hanging, and the Client does not accept 'timeout' option for remote_exec() 

"""

__version_info__ = ('0', '4', '0')
__version__ = '.'.join(__version_info__)


class Runner(object):

    def __init__(self, host, user=None, **kwargs):
        self.host = host
        self.user = user
        self.ssh = None
        self.sftp = None
        self.mgr = None
        self.auto_add = True

        forbidden = ['host', 'user', 'client', 'sftp', 'mgr']
        allowed = ['password', 'auto_add', 'timeout']
        for k, v in kwargs.items():
            if k in allowed and k not in forbidden:
                setattr(self, k, v)

        if not self.ssh:
            try:
                self.ssh = paramiko.SSHClient()
                if self.auto_add:
                    self.ssh.set_missing_host_key_policy(
                                                    paramiko.AutoAddPolicy())
                                                    
                self.ssh.connect(self.host, username=self.user)
            except Exception as e:
                raise e


    def close(self):
        if self.mgr:
            self.mgr.cleanup()
            
        self.sftp.close()
        self.ssh.close()
  
        
    """
    run()
    
    params:
        1. local script path/name
        2. sudo (True|False): default = False
        3. timeout (seconds): default = 10
        4. option string to be passed to remote shell command
    
    returns:
        1. exit code
        2. stdout lines as a list
        3. stderr lines as a list   
    """
    def run(self, local_script, sudo=False, timeout=10, opts=None):
        exit_code = 1

        if not os.path.exists(local_script):
            raise IOError (1, "File %s not found" % local_script)
            
        try:
            self.sftp = self.ssh.open_sftp()
        except Exception as e:
            raise e

        self.mgr = remotemanager.RemoteManager(self.sftp)
        self.mgr.install_remote_script(local_script)
        command_string = self.mgr.remote_script_path(local_script)

        if sudo:
            command_string = "sudo " + command_string

        if opts:
            command_string = command_string + " " + opts


        try:
            stdin, stdout, stderr = self.ssh.exec_command(command_string, 
                                                    timeout=timeout)
            exit_code = stdout.channel.recv_exit_status()
                                                       
        except Exception as e:
            raise e

        out = stdout.readlines()
        err = stderr.readlines()
        return (exit_code, out, err)
        


if __name__ == '__main__':
    
    opts = {}
    runargs = {}

    parser = argparse.ArgumentParser(description='Run local scripts on a remote host')
    parser.add_argument('host',
                                help='host to run script on')
    parser.add_argument('script',
                                help='path to local script to run on remote host')
    parser.add_argument('-u', '--user', 
                                help='user to connect to host as')
    parser.add_argument('-s', '--sudo', action='store_true', 
                                help='run remote script with sudo')
    parser.add_argument('-t', '--timeout', type=int,
                                help='timeout seconds for remote execution')
    parser.add_argument('-o', '--optargs', 
                                help='optional arguments to remote script')
    args = parser.parse_args()
   
    if not args.user:
        args.user = None
        
    if not args.timeout:
        args.timeout = None
       
    if not args.sudo:
        args.sudo = False
    
    
    runner = Runner(args.host, args.user)
    rval, out, err = runner.run(args.script, args.sudo,
                                            args.timeout, args.optargs)
    
    if out and out != "":
        print("".join(out))
    if err and err != "":
        sys.stderr.write("".join(err))
        
    runner.close()
    sys.exit(rval)

