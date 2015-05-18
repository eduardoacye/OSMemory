import os_system as sys
import os_utils as utl
            
class Simulator(object):
    def __init__(self):
        self.os = sys.OperatingSystem()

    def reloadOS(self):
        self.os = sys.OperatingSystem()

    def run(self, steps, start_func = utl.noop, during_func = utl.noop, end_func = utl.noop):
        start_func(self.os)
        for _ in xrange(steps):
            self.os.step()
            during_func(self.os)
        end_func(self.os)

    def debugRun(self, steps):
        self.run(steps, utl.debug, utl.debug, utl.noop)
