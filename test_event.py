import threading
import numpy
import time

from Globals import Global

def caller():
    while not G.end.is_set():
        G.respond.clear()
        wait_time = numpy.random.randint(1,10)
        print('Sleep timer:', wait_time)
        time.sleep(wait_time)
        G.call.set()
        G.respond.wait()
    return


if __name__ == "__main__":
    G = Global()
    t1 = threading.Thread(target=caller)
    t1.start()
    G.call.wait()
    print('Call Activated!')
    G.call.clear()
    G.respond.set()
    G.call.wait()
    print('Call Activated!')
    G.call.clear()
    G.end.set()
    G.respond.set()
    t1.join()
    print('All threads finished!')


