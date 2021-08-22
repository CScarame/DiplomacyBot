###################
# Globals.py
# Author: Sc4ry
# Function:
# list of Global variables, including event flags that are
# triggered by different programs.
###################

import threading

end = threading.Event()
call = threading.Event()
respond = threading.Event()

class Global:
    def __init__(self):
        self.end = threading.Event()
        self.call = threading.Event()
        self.respond = threading.Event()
        