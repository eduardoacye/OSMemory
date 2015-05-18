import urwid

palette = [('titlebar', 'black,bold', 'light cyan'),
           ('quit button', 'dark red,bold', 'default')]

header_text = urwid.Text(u'SIMULADOR DE MEMORIA CON PARTICIONES VARIABLES')
header = urwid.AttrMap(header_text, 'titlebar')

menu = urwid.Text([u'Presiona (', ('quit button', u'Q'), u') para salir.'])

main_text = urwid.Text(u'Bienvenido a mi proyecto final de SO')
main_filler = urwid.Filler(main_text, valign='top', top=1, bottom=1)
v_padding = urwid.Padding(main_filler, left=1, right=1)
main_box = urwid.LineBox(v_padding)

layout = urwid.Frame(header=header, body=main_box, footer=menu)

def handle_input(key):
    if key == 'Q' or key == 'q':
        raise urwid.ExitMainLoop()

main_loop = urwid.MainLoop(layout, palette, unhandled_input=handle_input)

main_loop.run()
