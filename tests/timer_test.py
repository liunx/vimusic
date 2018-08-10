#!/usr/bin/env python3

import time


for i in range(1000):
    pre = time.time()
    time.sleep(0.0011)
    cur = time.time()
    #print("sleep {}".format(cur - pre))


