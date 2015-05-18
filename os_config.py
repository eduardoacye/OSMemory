# This module contains the constants and important numbers for the
# system

# total blocks of physical memory
total_memory       = 256

# min blocks of memory a process can request
process_min_memory = 10

# max blocks of memory a process can request
process_max_memory = 50

# process min lifetime
process_min_lifetime = 5

# process max lifetime
process_max_lifetime = 20

# max rate of interactive processes (set to less than 1.0/2.0)
process_interactive_rate = 1.0/2.0

# process max rate of io burst (set to less than 1.0/2.0)
process_io_rate = 1.0/3.0       # of every 3 bursts 1 is io
