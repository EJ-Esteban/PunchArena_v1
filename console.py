import tkinter as tk
import myconstants as m_c

from types import FunctionType
from difflib import SequenceMatcher


class ConsoleWindow:
    # these functions are not considered for spell checking
    INTERNAL_FUNCTIONS = ["print", "find_match", "__init__", "resolve_cmd",
                          "send_cmd", "go_up", "go_down"]
    MATCH_THRESH = .6
    HR = "------------------------------"

    def __init__(self, root):
        frame = tk.Frame(root)
        frame.pack()
        root.wm_title("console")

        self.text = tk.Text(frame, bg="gray", width=50, height=20, font="courier 10", wrap="word", foreground="white",
                            bd=5)
        self.text.config(state="disabled")
        self.print("Punch Arena v." + m_c.VERSION_NUMBER + " Console\n")
        self.text.grid(row=0, column=0, sticky="NSEW")

        scroll = tk.Scrollbar(frame)
        self.text.configure(yscrollcommand=scroll.set)
        scroll.config(command=self.text.yview)
        scroll.grid(row=0, column=1, sticky="NSEW")

        self.cmdline = tk.Entry(frame, bg="gray", font="courier 10", foreground="white", bd=5)
        self.cmdline.grid(row=1, column=0, columnspan=2, sticky="SNEW")

        self.old_cmds = []
        self.rewind_level = 0
        self.temp_cmd = ""

        self.cmdline.bind("<Return>", self.send_cmd)
        self.cmdline.bind("<Up>", self.go_up)
        self.cmdline.bind("<Down>", self.go_down)

        self.function_list = [x for x, y in ConsoleWindow.__dict__.items() if type(y) == FunctionType]

    def print(self, message):
        self.text.config(state="normal")
        self.text.insert(tk.END, message + "\n")
        self.text.see(tk.END)
        self.text.config(state="disabled")

    def send_cmd(self, event):
        self.cmd = self.cmdline.get()
        self.cmdline.delete(0, tk.END)
        self.resolve_cmd()

    def resolve_cmd(self):
        message = self.cmd

        self.old_cmds.insert(0, message)
        self.rewind_level = 0
        self.temp_cmd = ""

        foo = message.partition(' ')[0]
        foo = foo.lower()
        message = self.cmd.replace(foo + " ", "", 1)
        self.print(foo + ":")
        if hasattr(self, foo) and (foo not in ConsoleWindow.INTERNAL_FUNCTIONS):
            getattr(self, foo)(message)
        else:
            self.print("ERROR-command \"" + foo + "\" not recognized.")
            self.find_match(foo)

    def find_match(self, foo):
        possibly = []
        for item in self.function_list:
            if item not in ConsoleWindow.INTERNAL_FUNCTIONS:
                ratio = SequenceMatcher(None, item, foo).ratio()
                if ratio > ConsoleWindow.MATCH_THRESH:
                    possibly.append(item)
        if len(possibly) > 0:
            message = "Perhaps you meant: "
            for s in possibly:
                message += '"' + s + '" '
            self.print(message)

    def go_up(self, event):
        if self.rewind_level == 0:
            self.temp_cmd = self.cmdline.get()
        if not self.rewind_level == len(self.old_cmds):
            self.rewind_level += 1
        if not self.rewind_level == 0:
            self.cmdline.delete(0, tk.END)
            self.cmdline.insert(tk.END, self.old_cmds[self.rewind_level - 1])

    def go_down(self, event):
        if not self.rewind_level == 0:
            self.rewind_level -= 1
        self.cmdline.delete(0, tk.END)
        if not self.rewind_level == 0:
            self.cmdline.insert(tk.END, self.old_cmds[self.rewind_level - 1])
        else:
            self.cmdline.insert(tk.END, self.temp_cmd)

    # command names are methods!
    def echo(self, items):
        """echoes given string"""
        if items == "@givehelp":
            self.print("echoes the user input")
        else:
            self.print(items)

    def die(self, items):
        """stops the process"""
        if items == "@givehelp":
            self.print("kills everything manually")
        else:
            exit()

    def help(self, items):
        """probes methods for their help"""
        if items == "@givehelp":
            self.print("okay, seriously, you're asking for help with the help function????")
        else:
            if hasattr(self, items):
                self.print("")
                getattr(self, items)("@givehelp")
            else:
                self.print("ERROR: \"" + items + "\" not recognized.")
                self.find_match(items)

    def clear(self, items):
        """clears the console"""
        if items == "@givehelp":
            self.print("clears the console")
        else:
            self.text.config(state="normal")
            self.text.delete(1.0, tk.END)
            self.text.config(state="disabled")
            self.print(ConsoleWindow.HR)

    def clean(self, items):
        """clears the console and commands"""
        if items == "@givehelp":
            self.print("clears the console and removes old command records")
        else:
            self.old_cmds = []
            self.rewind_level = 0
            self.temp_cmd = ""
            self.clear("")


if __name__ == "__main__":
    # you can try some rudimentary controls without a game attached. mostly echo and die.
    root = tk.Tk()
    root.resizable(0, 0)
    ConsoleWindow(root)
    root.mainloop()
