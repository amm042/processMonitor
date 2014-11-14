import psutil

def filter_if_alive(procs):
    sproc = set(procs)
    attrs = ['name', 'exe', 'cmdline']
    for p in psutil.process_iter():
        try:
            pinfo = p.as_dict(attrs, ad_value='')
        except psutil.NoSuchProcess:
            print ('got ex')
            pass
        else:
            k = " ".join(pinfo['cmdline'])
            if k in sproc:
                sproc.remove(pinfo['cmdline'])
            
    return list(sproc)
def main():
    
    procs = [
             ('python', 'pywattnodeLogger.py', 'pywattnode.conf' ),
             ]
    
    for proc in filter_if_alive(procs):
        print ("need to spawn", proc)


if __name__ == "__main__":
    main()