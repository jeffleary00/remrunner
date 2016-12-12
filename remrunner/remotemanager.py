from __future__ import unicode_literals
import os
import sys
import paramiko


class RemoteManager():

    def __init__(self, sftp):
        self.sftp = sftp
        self.targetdir = os.path.join('.remrunner', str(os.getpid()))
        try:
            self.mkdir_p(self.sftp, self.targetdir)
        except Exception as e:
            print(type(e))
            print(e)
            raise 
            

    def cleanup(self):
        try:
            files = self.sftp.listdir(self.targetdir)
            for f in files:
                self.sftp.remove("%s/%s" % (self.targetdir, f))
        
            self.sftp.rmdir(self.targetdir)
        except Exception as e:
            print(e)
            pass
            
    
    def install_remote_script(self, local_script):
        try:
            self.sftp.put(local_script, self.remote_script_path(local_script))
            self.sftp.chmod(self.remote_script_path(local_script), 0o700)
        except Exception as e:
            raise e
        

    def remove_remote_script(self, script):
        self.sftp.remove(script)
        pass


    def remote_dir(self, script):
        return self.targetdir


    def remote_script_path(self, local_script):
        atoms = os.path.split(local_script)
        return os.path.join(self.targetdir, atoms[-1])


    """
    mkdir_p()
    
    recursively create a remote directory tree via SFTP. 
    copies behaviour of mkdir -p

    params:
        1. an active sftp client object
        2. name of remote directory path

    returns:
        
    """
    def mkdir_p(self, sftp, remote, is_dir=True):
        dirs_ = []
        if is_dir:
            dir_ = remote
        else:
            dir_ = os.path.split(remote)
        
        while len(dir_) > 1:
            dirs_.append(dir_)
            dir_, _  = os.path.split(dir_)

        if len(dir_) == 1 and not dir_.startswith("/"): 
            dirs_.append(dir_)

        while len(dirs_):
            dir_ = dirs_.pop()
            try:
                sftp.stat(dir_)
            except:
                sftp.mkdir(dir_, 0o700)


