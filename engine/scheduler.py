import time

from engine.sched_mgr.sched_mgr import Sched_Child

s = Sched_Child(time.time, time.sleep)