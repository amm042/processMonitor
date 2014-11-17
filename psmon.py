#!/usr/bin/python
import psutil
import subprocess
import os
import logging
import shlex 

logging.basicConfig(level = logging.DEBUG)
LOG = logging.getLogger("psmon")

def filter_if_alive(procs):    
    sproc = set([" ".join(p) for p in procs])
    #LOG.debug("<-- " + str(sproc))
    attrs = ['name', 'exe', 'cmdline']
    for p in psutil.process_iter():
        try:
            pinfo = p.as_dict(attrs, ad_value='')
        except psutil.NoSuchProcess:
            print ('got ex')
            pass
        else:
            k = " ".join(pinfo['cmdline'])
                        
            #if 'python' in k:
                #LOG.debug("--> " + k)
            if k in sproc:
                sproc.remove(k)
            
    return list(sproc)

def spawn(proc):
    
    print 'spawn', proc
    try:
        p = subprocess.Popen(shlex.split(proc), 
                             stdout = subprocess.PIPE, 
                             stderr = subprocess.PIPE, 
                             close_fds = True,
                             preexec_fn = os.setsid)
        if p.pid > 0:
            LOG.info("spawned " + str(proc))
        else:
            LOG.error("spawn failed")
        
    except OSError, e:
        LOG.error("Spawn failed: " + str(e))
    
    print 'done'
    
def main():
    
    procs = [
             ('/usr/bin/python', '/home/alan/Src/python/pywattnode/pywattnodeLogger.py', '/home/alan/Src/python/pywattnode/pywattnode.conf' ),
             ]
        
    for proc in filter_if_alive(procs):
        spawn(proc)


if __name__ == "__main__":
    main()