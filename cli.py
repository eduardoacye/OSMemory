from urwid import *

def handle_input(key):
    if key in ('q', 'Q'):
        raise ExitMainLoop()

def play_simulation(button):
    sidebar_info_text.set_text(u'Corriendo simulacion')

def pause_simulation(button):
    sidebar_info_text.set_text(u'Simulacion suspendida')

def restart_simulation(button):
    sidebar_info_text.set_text(u'Simulacion reiniciada')

def quit_simulator(button):
    raise ExitMainLoop()

def block_selected(button, addr):
    sidebar_info_text.set_text(u'Bloque de memoria con direccion ('+str(addr)+')')

# COLOR SCHEME
palette = [('title', 'dark green,bold', 'black'),
           ('about', 'dark green,bold', 'black'),
           ('select', 'dark green,bold', 'black'),
           ('text', 'white', 'black')]

# TITLE
title = AttrMap(Text(u'OSMemory', align='center'), 'title')

# CONTACT/ABOUT
about = AttrMap(Text(u'Eduardo Acuna Yeomans (eduardo.acye@gmail.com) 2015 Proyecto final de Sistemas Operativos'),
                'about')




# SIDEBAR

sidebar_menu_list = ListBox(SimpleFocusListWalker([AttrMap(Button(u'Iniciar', play_simulation),
                                                           None, focus_map='select'),
                                                   AttrMap(Button(u'Detener', pause_simulation),
                                                           None, focus_map='select'),
                                                   AttrMap(Button(u'Reiniciar', restart_simulation),
                                                           None, focus_map='select'),
                                                   Divider(),
                                                   Divider(u'\N{HORIZONTAL BAR}'),
                                                   Divider(),
                                                   AttrMap(Button(u'Salir', quit_simulator),
                                                           None, focus_map='select')]))


sidebar_menu = LineBox(Padding(sidebar_menu_list, left=2, right=2), 'menu')

sidebar_info_text = Text(u'', align='left')
sidebar_info = LineBox(Filler(sidebar_info_text, valign='top'), 'informacion')

sidebar_layout = Pile([('weight', 1, sidebar_menu), ('weight', 2, sidebar_info)])

sidebar = Overlay(sidebar_layout, SolidFill(u'\N{MEDIUM SHADE}'),
                  align='center', width=('relative', 95),
                  valign='middle', height=('relative', 95))





# SIMULATION BOX

memblocks = [AttrMap(Button(hex(i), block_selected, i), None, focus_map='select') for i in xrange(256)]
simulbox_memory_view = GridFlow(memblocks, 8, 1, 0, 'center')

#simulbox_memory_view = GridFlow([Text(u'A'), Text(u'B'), Text(u'C'), Text(u'D')],
#                                2, 1, 1, 'center')

simulbox_memory = LineBox(Columns([Filler(simulbox_memory_view), SolidFill(u'o')], 2), 'memoria')
#simulbox_memory = LineBox(Columns([SolidFill(u'x'), SolidFill(u'o')], 2), 'memoria')

simulbox_processes = LineBox(Filler(Text(u'Sobre los procesos', align='center')), 'procesos')
simulbox_components = LineBox(Filler(Text(u'Componentes de la maquina', align='center')), 'componentes')

simulbox_layout = Pile([simulbox_memory,
                        Columns([('weight', 2, simulbox_processes), ('weight', 1, simulbox_components)])])


simulbox = Overlay(simulbox_layout, SolidFill(u'\N{DARK SHADE}'),
                   align='center', width=('relative', 99),
                   valign='middle', height=('relative', 95))





hlayout = Columns([('weight', 1, sidebar), ('weight', 4, simulbox)])



content = Overlay(hlayout, SolidFill(u'\N{LIGHT SHADE}'),
                  align='center', width=('relative', 99),
                  valign='middle', height=('relative', 99))

main_layout = Frame(header=title, body=content, footer=about)

loop = MainLoop(main_layout, palette, unhandled_input=handle_input)

loop.run()
