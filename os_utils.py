def index_max(lst, selector):
    return max(xrange(len(lst)), key=lambda x: selector(lst.__getitem__(x)))

def index_min(lst, selector):
    return min(xrange(len(lst)), key=lambda x: selector(lst.__getitem__(x)))

def noop(os):
    pass

def debug(os):
    print os
    print '\n'
