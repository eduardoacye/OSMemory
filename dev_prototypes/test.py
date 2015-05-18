import curses

stdscr = curses.initscr()

curses.noecho()
curses.cbreak()
curses.curs_set(0)

if curses.has_colors():
    curses.start_color()

curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)

stdscr.addstr("Simulador de memoria con particiones variables", curses.A_REVERSE)
stdscr.chgat(-1, curses.A_REVERSE)

stdscr.addstr(curses.LINES-1, 0, "Presiona Q para salir")

stdscr.chgat(curses.LINES-1, 7, 1, curses.A_BOLD | curses.color_pair(2))
stdscr.chgat(curses.LINES-1, 9, 1, curses.A_BOLD | curses.color_pair(1))

main_window = curses.newwin(curses.LINES-2, curses.COLS, 1, 0)

main_text_window = main_window.subwin(curses.LINES-6, curses.COLS-4, 3, 2)

main_text_window.addstr("Bienvenido a mi proyecto final de SO")

main_window.box()

stdscr.noutrefresh()
main_window.noutrefresh()

curses.doupdate()

while True:
    c = main_window.getch()

    if c == ord('q') or c == ord('Q'):
        break

    stdscr.noutrefresh()
    main_window.noutrefresh()
    main_text_window.noutrefresh()
    curses.doupdate()

curses.nocbreak()
curses.echo()
curses.curs_set(1)

curses.endwin()

