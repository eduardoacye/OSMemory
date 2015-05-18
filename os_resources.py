# This module contains the machine resources. These are managed by the
# from the operating_system module

from operator import itemgetter
from itertools import groupby

import os_config as conf
import os_utils as utl

class Memory(object):
    def __init__(self):
        # amount of blocks in physical memory
        self.total = conf.total_memory
        self.available = conf.total_memory

        self.used = {}
        self.free = [(0,conf.total_memory)]

    def __str__(self):
        s = 'MEMORY ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
        s += 'total = ' + str(self.total) + '\n'
        s += 'available = ' + str(self.available) + '\n'
        s += 'used partitions............................\n' + str(self.used) + '\n'
        s += 'free partitions............................\n' + str(self.free)
        return s
    def __repr__(self):
        return 'Memory(total='+str(self.total)+',available='+str(self.available)+')'
        
    def worst_fit(self):
        return utl.index_max(self.free, lambda x: x[1])

    def assign(self, pid, blocks, i):
        if blocks > self.free[i][1]:
            raise Exception('Esa particion no tiene suficiente espacio disponible')
        self.available = self.available-blocks
        self.used[pid] = (self.free[i][0], blocks)
        self.free[i] = (self.free[i][0]+blocks, self.free[i][1]-blocks)
        
    def release(self, pid):
        occ = self.used[pid]
        del self.used[pid]
        self.free.append(occ)
        self.fusion_memory()
        self.available = self.available+occ[1]

    def fusion_memory(self):
        self.free.sort(key=lambda x: x[0])
        grouped = []
        for k, g in groupby(enumerate (sum(map(lambda x: range(x[0],x[0]+x[1]), self.free), [])),
                            lambda (i,x):i-x):
            grouped.append(map(itemgetter(1), g))
        self.free = map(lambda arr: (arr[0], arr[len(arr)-1]-arr[0]+1), grouped)

class CPU(object):
    def __init__(self):
        self.process = 0

    def __repr__(self):
        return 'CPU(pid = ' + str(self.process.id if self.occupied() else 'None') + ')'

    def tock(self):
        if not self.occupied():
            return
        if self.process.burst and self.process.burst[0] == 'cpu':
            self.process.burst.pop(0)
            self.process.lived += 1

    def assign(self, process):
        p = self.process
        self.process = process
        return p

    def release(self):
        p = self.process
        self.process = 0
        return p

    def occupied(self):
        return self.process != 0

    def finished(self):
        return self.ended() or self.process.burst[0] != 'cpu'

    def ended(self):
        if not self.occupied():
            return True
        return not self.process.burst

class IODevice(object):
    def __init__(self):
        self.process = 0

    def __repr__(self):
        return 'IODevice(pid = ' + str(self.process.id if self.occupied() else 'None') + ')'

    def tock(self):
        if not self.occupied():
            return
        if self.process.burst and self.process.burst[0] == 'io':
            self.process.burst.pop(0)
            self.process.lived += 1

    def assign(self, process):
        p = self.process
        self.process = process
        return p

    def release(self):
        p = self.process
        self.process = 0
        return p

    def occupied(self):
        return self.process != 0

    def finished(self):
        return self.ended() or self.process.burst[0] != 'io'

    def ended(self):
        if not self.occupied():
            return True
        return not self.process.burst

