import os
import sys
import datetime

def child(pid):
    print('child PID:', pid)
    
if __name__ == '__main__':
    print('Arguments: {}'.format(sys.argv))
    time_str = sys.argv[1:2].join()
    print(time_str)
    child(os.getpid())
    print('Child Done!')