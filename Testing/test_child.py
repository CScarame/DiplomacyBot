import os
import sys
import datetime

def child(pid):
    print('child PID:', pid)
    
if __name__ == '__main__':
    print('Arguments: {}'.format(sys.argv))
    child(os.getpid())
    print('Child Done!')