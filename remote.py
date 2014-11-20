"""Remote control for raspberry pi dataloggers

Alan Marchiori
"""

import paramiko


def run(node, cmd):
    c = paramiko.SSHClient()
    #c.load_system_host_keys()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
    c.connect(node, username = 'pi', password = 'raspberry')
    stin,stout,sterr = c.exec_command(cmd)

    print sterr.readlines()
    print stout.readlines()

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

nodes = ['amm-61a80a', 'amm-ce4440', 'amm-4fd239', 'amm-903c01']

for node in nodes:    
    #format_dfs(node)
    #start_hadoop(node)
    start_opentsdb(node)