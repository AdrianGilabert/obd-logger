import curses
from OBDLogger import OBDLogger


def main(stdscr):
    logger = OBDLogger(stdscr)
    logger.main()


curses.wrapper(main)
