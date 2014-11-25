"""Remote control for raspberry pi dataloggers

Alan Marchiori
"""

import paramiko

import os.path

def run(node, cmd):
    c = paramiko.SSHClient()
    #c.load_system_host_keys()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
    c.connect(node, username = 'pi', password = 'raspberry')
    stin,stout,sterr = c.exec_command(cmd)

    print sterr.readlines()
    print stout.readlines()
    c.close()
def scp(remote_src, local_dest):
    
    node, remote_path = remote_src.split(':')
    
    c = paramiko.Transport((node, 22))
    #c.load_system_host_keys()
    #c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
    print 'connecting to', node

    c.connect( username = 'pi', password = 'raspberry')    
    
    sftp = paramiko.SFTPClient.from_transport(c)
    
    sftp.get(remote_path, local_dest)
    sftp.close()
    
    c.close()
    
    
def format_dfs(node):
    # maybe this should stop hadoop first?
    run (node, "rm -rf /app/hadoop/tmp/dfs; rm -rf /app/hadoop/tmp/nm-local-dir; /usr/local/hadoop/bin/hadoop namenode -format")    

def start_hadoop(node):
    # only start on master node
    if node == 'amm-61a80a':
        run (node, '/usr/local/hadoop/sbin/start-all.sh')
        
def start_opentsdb(node):
    # this makes sure permissions are correct
    # then starts opentsdb in a screen session
    run (node, 'sudo chown pi:pi /tmp/opentsdb; /usr/bin/screen -dm /usr/share/opentsdb/bin/tsdb tsd')


def start_pywatt(node):
    
    run(node, '/usr/bin/screen -dm /usr/bin/python /home/pi/pywattnode/pywattnodeLogger.py /home/pi/pywattnode/pywattnode.conf')
def start_zookeeper(node):
    run(node, '/usr/local/zookeeper/bin/zkServer.sh stop; rm -rf /usr/local/zookeeper/data/version-2; rm /usr/local/zookeeper/data/zookeeper_server.pid; /usr/local/zookeeper/bin/zkServer.sh start')
       
nodes = ['amm-61a80a', 'amm-ce4440', 'amm-4fd239', 'amm-903c01']

def get_logs(node, path = './logs'):
    scp ("{}:{}".format(node, '/var/log/opentsdb/opentsdb.log'), 
         os.path.join(path, '{}-opentsdb.log'.format(node)))

for node in nodes:    
    #format_dfs(node)
    start_zookeeper(node)
    #start_hadoop(node)
    #start_opentsdb(node)
    #start_pywatt(node)
    
    #get_logs(node)
    
    
    