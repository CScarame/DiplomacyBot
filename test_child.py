import os
import time

def child(pid):
    print('child PID:', pid)
    
if __name__ == '__main__':
    child(os.getpid())
    print('Child Done!')