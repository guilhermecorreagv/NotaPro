import tkinter as tk
from src.menu import add_menu
from src.toolbar import add_toolbar
from src.db import connect_database, setup_database
import os
import config


if __name__ == '__main__':
    # Creates window
    config.window = tk.Tk()
    window = config.window
    window.title("NotaPro Versão 0.1")
    config.CWD = os.getcwd()

    connect_database()
    # setup_database()

    add_menu()
    add_toolbar()


    window.attributes('-zoomed', True) # makes GUI open up to screen size
    window.mainloop()
