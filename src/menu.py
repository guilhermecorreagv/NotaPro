import tkinter as tk
import config 

def add_inventory():
    sub_window = tk.Toplevel(config.window)
    sub_window.title("Adicionar Estoque")

    # @TODO: See if this fixed size window is a good idea
    sub_window.geometry("800x600")

        # Add widgets for CRUD operations
    lbl = tk.Label(sub_window, text="CRUD Operations", font=("Helvetica", 16))
    lbl.pack(pady=10)

    # Add Entry widget for data input
    entry = tk.Entry(sub_window)
    entry.pack(pady=10)

    # Add buttons for Create, Read, Update, Delete
    def create():
        data = entry.get()
        print(f"Create: {data}")

    def read():
        print("Read operation")

    def update():
        data = entry.get()
        print(f"Update: {data}")

    def delete():
        print("Delete operation")

    btn_create = tk.Button(sub_window, text="Create", command=create)
    btn_create.pack(pady=5)

    btn_read = tk.Button(sub_window, text="Read", command=read)
    btn_read.pack(pady=5)

    btn_update = tk.Button(sub_window, text="Update", command=update)
    btn_update.pack(pady=5)

    btn_delete = tk.Button(sub_window, text="Delete", command=delete)
    btn_delete.pack(pady=5)

def add_menu():
    # Creates menu bar
    main_menu_bar = tk.Menu(config.window)
    # Adds fields
    main_menu_fields = [
        "Arquivos",
        "Estoque",
        "Pré-Venda",
        "Depto Pessoal",
        "Patrimonio",
        "Utilitários"
    ]

    # initialize empty commands
    main_menu_commands = {}
    for field in main_menu_fields:
        main_menu_commands[field] = {}

    # add commands here
    main_menu_commands["Arquivos"]["Consultar Arquivo"] = lambda *args: None
    main_menu_commands["Arquivos"]["Adicionar Arquivo"] = lambda *args: None
    main_menu_commands["Arquivos"]["Remover Arquivo"] = lambda *args: None
    main_menu_commands["Estoque"]["Consultar Estoque"] = lambda *args: None
    main_menu_commands["Estoque"]["Adicionar Estoque"] = add_inventory
    main_menu_commands["Estoque"]["Remover Estoque"] = lambda *args: None
    

    # Add menu options
    menus = []
    for field in main_menu_fields:
        menus.append(tk.Menu(main_menu_bar, tearoff=0))
        for name, func in main_menu_commands[field].items():
            menus[-1].add_command(label=name, command=func)

        state = 'normal' if len(main_menu_commands[field]) > 0 else 'disabled'
        main_menu_bar.add_cascade(label=field, menu=menus[-1], state=state)

    config.window.config(menu=main_menu_bar)