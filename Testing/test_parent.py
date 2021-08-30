import os
import datetime
from multiprocessing import Process

def parent(pid):
    print('parent PID:', pid)
    
if __name__ == '__main__':
    currentTime = datetime.datetime.today()
    print(str(currentTime))
    print(currentTime)
    parent(os.getpid())
    p = os.system('python ./Testing/test_child.py')
    print('Parent says child is ', p)
    print('Parent Done!')
    print(currentTime)
