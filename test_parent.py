import os
import subprocess
from multiprocessing import Process

def parent(pid):
    print('parent PID:', pid)
    
if __name__ == '__main__':
    parent(os.getpid())
    p = os.system('python .\\test_child.py')
    print('Parent says child is ', p)
    print('Parent Done!')
