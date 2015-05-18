from urwid import *

texts = {
    
}

class CLI(object):
    def __init__(self):
        self.loop = MainLoop(app_layout, palette, unhandled_input=self.handle_input)
