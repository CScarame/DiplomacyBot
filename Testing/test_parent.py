import os
import datetime
from multiprocessing import Process

def parent(pid):
    print('parent PID:', pid)
    
if __name__ == '__main__':
    currentTime = datetime.datetime.today()
    extraMinute = datetime.timedelta(seconds=60-currentTime.second,microseconds=1000000-currentTime.microsecond)
    futureTime = currentTime + extraMinute
    print(currentTime)
    print(futureTime)
    parent(os.getpid())
    p = os.system('python ./Testing/test_child.py')
    print('Parent says child is ', p)
    print('Parent Done!')
    print(currentTime)
