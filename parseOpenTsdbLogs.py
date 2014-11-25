import re

import matplotlib.pyplot as plt
import numpy

def parse(fname, reg):
    r = re.compile(reg)
    text = open(fname, 'r').read()
        
    times =[]
    
    for line in r.findall(text):
        
        
        ms = int(line.split()[-1][0:-2])/1000.0
        
        
        #print(line.strip(), '==', ms)
        times.append(ms)


    #print (line.strip())
    print ("{} matches in {}".format(len(times), fname))
    return times
    

def main():
    
    logs = ['logs/amm-61a80a-opentsdb.log',
            'logs/amm-ce4440-opentsdb.log',
            'logs/amm-4fd239-opentsdb.log',
            'logs/amm-903c01-opentsdb.log',
            ]
    
    stats= []
    labels = []
    for log in logs:
        m =parse(log, '/api/put.*ms')
        if len(m)> 0:
            stats+=m
            labels.append(log)
        else:
            print("warn: {} has no matches.".format(log))
        
    #print stats
    
    fig, ax = plt.subplots(figsize=(3,5))
    ax.boxplot(stats, labels = [''])
    ax.set_ylim((0,3))
    ax.set_title('Insert Time')
    ax.set_ylabel('Seconds')
    
    print 'mean =', numpy.mean(stats)
    print 'median = ', numpy.median(stats)
    print 'std = ', numpy.std(stats)
    
    print 'over 1', len(filter(lambda x: x > 1.0, stats)), 'of', len(stats)
    print 'under 1', len(filter(lambda x: x <= 1.0, stats)), 'of', len(stats) 
    
    #plt.show()

if __name__ == "__main__":
    main()