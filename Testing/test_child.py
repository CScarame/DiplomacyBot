import os
import sys
import time
import datetime

def child(pid):
    print('child PID: {}'.format(pid))
    
if __name__ == '__main__':
    print('Arguments: {}'.format(sys.argv))
    time_str = " ".join(sys.argv[1:])
    print(time_str)
    goalTime = datetime.datetime.strptime(time_str)
    while True:
        currentTime = datetime.datetime.now()
        if(goalTime < currentTime):
            break
        time.sleep(1)
    child(os.getpid())
    print('Child Done!')