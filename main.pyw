from game_core import Game
import tkinter as tk
from console import ConsoleWindow

CONSOLE = True

if __name__=="__main__":

    root = tk.Tk()
    root.resizable(0,0)
    Game(root)

    if CONSOLE:
        c = tk.Toplevel(root)
        ConsoleWindow(c)
        c.geometry("%dx%d+%d+%d" % (430,360,root.winfo_rootx()+700,root.winfo_rooty()))

    root.mainloop()
