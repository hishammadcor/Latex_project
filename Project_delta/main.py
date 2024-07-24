
import tkinter as tk
from GUI.UI_tk import LaTeXTableGeneratorUI


if __name__ == "__main__":
    root_window = tk.Tk()
    app = LaTeXTableGeneratorUI(root_window)
    root_window.mainloop()
