#!/usr/bin/env python3

import threading
import queue
import time


def worker(q):
    """thread worker function"""
    while True:
        if not q.empty():
            item = q.get_nowait()
            print(item)
            q.task_done()
            if item == 99:
                break
        time.sleep(0.001)


if __name__ == "__main__":
    q = queue.Queue()
    t = threading.Thread(target=worker, args=(q,))
    t.start()
    for i in range(10):
        q.put([1,2,3])
        time.sleep(1)
    q.put(99)
