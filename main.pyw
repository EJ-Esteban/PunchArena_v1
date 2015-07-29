from game_core import Game
import tkinter as tk
from console import ConsoleWindow

from myconstants import CONSOLE_WINDOW_ENABLED

CONSOLE = True

if __name__ == "__main__":

    root = tk.Tk()
    root.resizable(0, 0)
    game = Game(root)

    if CONSOLE_WINDOW_ENABLED:
        c = tk.Toplevel(root)
        console = ConsoleWindow(c)
        c.geometry("%dx%d+%d+%d" % (430, 360, root.winfo_rootx() + 700, root.winfo_rooty()))
        console.attach_game(game)

    root.mainloop()
