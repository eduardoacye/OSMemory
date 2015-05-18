# This module contains the minimalistic operating system logic
from random import randint
import os_config as conf
import os_resources as res
import os_structures as ds

class OperatingSystem(object):
    def __init__(self):
        self.memory = res.Memory()
        self.cpu = res.CPU()
        self.io = res.IODevice()
        self.new_queue = ds.NewQueue()
        self.st_queue = ds.ShortTermQueue()
        self.waiting_queue = ds.WaitingQueue()
        self.lt_queue = ds.LongTermQueue()
        self.id_count = 0

    def __repr__(self):
        return 'OperatingSystem()'
    
    def __str__(self):
        s = '=================================================\n'
        s+= 'OPERATING SYSTEM ================================\n'
        s+= '=================================================\n'
        s+= self.memory.__str__() + '\n'
        s+= 'QUEUES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
        s+= self.new_queue.__repr__() + '\n'
        s+= self.waiting_queue.__repr__() + '\n'
        s+= self.st_queue.__repr__() + '\n'
        # s+= self.lt_queue.__repr__() + '\n'
        s+= '================================================='
        return s

    def next_id(self):
        self.id_count += 1
        return self.id_count

    def incoming_process(self):
        self.handle_new()
        self.handle_creation()

    def work(self):
        self.cpu_tick()
        self.io_tick()
        self.handle_ready()
        self.handle_waiting()
    
    def step(self):
        self.incoming_process()
        self.work()

    def terminate(self, pid):
        self.memory.release(pid)
        self.handle_sleeping()

    def cpu_tick(self, times = -1):
        if not self.cpu.occupied():
            return
        repeats = conf.process_max_lifetime if times == -1 else times
        for t in range(repeats):
            self.cpu.tock()
            if self.cpu.ended():
                p = self.cpu.release()
                self.terminate(p.id)
                return
            elif self.cpu.finished():
                p = self.cpu.release()
                self.waiting_queue.enqueue(p)
                return

    def io_tick(self, times = -1):
        if not self.io.occupied():
            return
        repeats = conf.process_max_lifetime if times == -1 else times
        for t in range(repeats):
            self.io.tock()
            if self.io.ended():
                p = self.io.release()
                self.terminate(p.id)
                return
            elif self.io.finished():
                p = self.io.release()
                self.st_queue.enqueue(p)
                return
            
    def handle_ready(self):
        if self.cpu.occupied():
            if self.cpu.finished():
                p = self.cpu.release()
                self.st_queue.enqueue(p)
            else:
                return
        if not self.st_queue.empty():
            p = self.st_queue.dequeue()
            self.cpu.assign(p)
        

    def handle_waiting(self):
        if self.io.occupied():
            if self.io.finished():
                p = self.io.release()
                self.st_queue.enqueue(p)
            else:
                return
        if not self.waiting_queue.empty():
            p = self.waiting_queue.dequeue()
            self.io.assign(p)

    def handle_new(self):
        if self.new_queue.size() < 10:
            self.new_queue.enqueue((self.next_id(),
                                    randint(conf.process_min_lifetime, conf.process_max_lifetime),
                                    randint(conf.process_min_memory, conf.process_max_memory)))
    def handle_creation(self):
        if self.memory.available < self.new_queue.peek()[2]:
            return -1
        
        elm = self.new_queue.dequeue()
        p = ds.Process(elm[0], elm[1], elm[2])

        i = self.memory.worst_fit()
        if self.memory.free[i][1] >= p.memory_blocks:
            self.memory.assign(p.id, p.memory_blocks, i)
            self.st_queue.enqueue(p)
        else:
            self.lt_queue.enqueue(p)

    def handle_sleeping(self):
        if self.lt_queue.empty():
            return
        p = self.lt_queue.peek()
        i = self.memory.worst_fit()
        if self.memory.free[i][1] >= p.memory_blocks:
            self.memory.assign(p.id, p.memory_blocks, i)
            self.st_queue.enqueue(p)
            self.lt_queue.dequeue()
