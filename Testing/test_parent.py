import os
import sys
import datetime
from multiprocessing import Process

def parent(pid):
    print('parent PID: {}'.format(pid))
    
if __name__ == '__main__':
    currentTime = datetime.datetime.today()
    futureTime = currentTime.replace(second=0, microsecond=0) + datetime.timedelta(minutes=1)
    print(futureTime)
    parent(os.getpid())
    p = os.system('python ./Testing/test_child.py {}'.format(str(futureTime)))
    print('Parent Done!')
    print(futureTime)
