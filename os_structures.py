# This module contains the data structures used by the system.

import os_config as conf
from collections import deque
from random import randint

class Process(object):
    def __init__(self, id, lifetime, memory_blocks):
        self.id = id
        self.memory_blocks = memory_blocks
        self.interactive = False if randint(0,int(1/conf.process_interactive_rate -1)) else True
        
        self.lifetime = lifetime
        self.lived = 0
        
        if self.interactive:
            self.burst = ['cpu' if randint(0,int(1/conf.process_io_rate - 1)) else 'io'
                          for i in range(self.lifetime)]
        else:
            self.burst = ['cpu' for i in range(self.lifetime)]
    def __repr__(self):
        return 'Proces(pid='+str(self.id)+',mem='+str(self.memory_blocks)+',intr='+str(self.interactive)+')'

class FIFOQueue(object):
    def __init__(self):
        self.queue = deque()
        
    def enqueue(self, elm):
        self.queue.append(elm)
        
    def dequeue(self):
        return self.queue.popleft()
    
    def peek(self):
        return self.queue[0]
    
    def processes(self):
        return list(self.queue)

    def empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)
            
class WaitingQueue(FIFOQueue):
    """
    Straightforward FIFO queue for the processes waiting for a IO device
    """
    def __repr__(self):
        return 'WaitingQueue(' + str(self.processes()) + ')'
        
class NewQueue(FIFOQueue):
    """
    Straightforward FIFO queue for the processes being created
    """
    def __repr__(self):
        return 'NewQueue(' + str(self.processes()) + ')'

class ShortTermQueue(FIFOQueue):
    """
    Multilevel queue for the CPU short-time scheduling
    """
    def __repr__(self):
        return 'ShortTermQueue(' + str(self.processes()) + ')'

class LongTermQueue(FIFOQueue):
    """
    Shortest job first queue with ageing for the CPU long-term scheduling
    """
    def __repr__(self):
        return 'LongTermQueue(' + str(self.processes()) + ')'
