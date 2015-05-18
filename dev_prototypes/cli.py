from urwid import *
"""
palette = [('title style', 'dark green,bold', 'black'),
           ('command style', 'dark magenta,bold', 'black'),
           ('bg', 'white', 'dark cyan')]

title_text = urwid.Text(('title style', u'OSMemory'), align='center')
title_text_map = urwid.AttrMap(title_text, 'title style')
title_fill = urwid.Filler(title_text_map, 'top')
title_fill_map = urwid.AttrMap(title_fill, 'bg')

command_text = urwid.Text(('command style', u'> '), align='left')
command_text_map = urwid.AttrMap(command_text, 'command style')
command_fill = urwid.Filler(command_text_map, 'bottom')
command_fill_map = 


def key_interceptor(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

loop = urwid.MainLoop(title_fill_map, palette, unhandled_input=key_interceptor)
loop.run()
"""

# COLOR PALETTE
palette = [('title', 'dark green,bold', 'black'),
           ('command', 'dark magenta,bold', 'black'),
           ('bg', 'black', 'light gray')]


# TITLE
title_text = Text(u'OSMemory', align='center')
title = AttrMap(title_text, 'title')

# MINIBUFFER
command_text = Text(('title', u'> '))
command = AttrMap(command_text, 'command')

# WELCOME
welcome_text = Text(u'Bienvenido al simulador de memoria con particiones variables.\n\nPara salir del programa presiona la tecla (Q).', align='center')
welcome_filler = Filler(welcome_text, valign='top', top=1, bottom=1)
welcome = AttrMap(welcome_filler, 'bg')
padding = Padding(welcome, left=1, right=1)
welcome_box = LineBox(padding)

# MENU
def run_sim(button):
    welcome_filler.original_widget = Text(u'ASDASD')

def config(button):
    pass

menu_body = [Text(('title',u'Menu'), align='center'), Divider()]
button = Button(u'Correr simulador', run_sim)
menu_body.append(AttrMap(button, None, focus_map='title'))
button = Button(u'Configuracion', config)
menu_body.append(AttrMap(button, None, focus_map='title'))
main = Padding(ListBox(SimpleFocusListWalker(menu_body)), left=2, right=2)
menu = Overlay(main, SolidFill(u'\N{MEDIUM SHADE}'),
               align='center', width=('relative', 10),
               valign='middle', height=('relative', 10),
               min_width=20, min_height=9)

#pile = Pile([welcome_box, menu])
pile = Pile([welcome_box, main])



asd = Overlay(pile, SolidFill(#SolidFill(u'\N{MEDIUM SHADE}'),
              align='center', width=('relative', 90),
              valign='middle', height=('relative', 90))


layout = Frame(header=title, body=pile, footer=command)

def handle_input(key):
    if key in ('q', 'Q'):
        raise ExitMainLoop()

loop = MainLoop(layout, palette, unhandled_input=handle_input)

loop.run()
