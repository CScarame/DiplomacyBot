import os
import sys
import datetime
import subprocess
import time
#from multiprocessing import Process

def parent(pid):
    print('parent PID: {}'.format(pid))
    
if __name__ == '__main__':
    currentTime = datetime.datetime.today()
    futureTime = currentTime.replace(second=0, microsecond=0) + datetime.timedelta(minutes=1)
    print(futureTime)
    parent(os.getpid())
    child = subprocess.Popen('python3 ./Testing/test_child.py {}'.format(str(futureTime)).split())
    while child.poll() == None:
        print('Parent waiting for child...')
        time.sleep(5)
    #p = os.system('python ./Testing/test_child.py {}'.format(str(futureTime)))
    print('Parent Done!')
    print(futureTime)
