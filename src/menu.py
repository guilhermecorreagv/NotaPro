import tkinter as tk
from tkinter import ttk, messagebox
import config 

# Function to fetch data from the database
def fetch_data(page, page_size):
    offset = (page - 1) * page_size
    con = config.db_connection
    cur = con.cursor()
    cur.execute("SELECT * FROM Products LIMIT ? OFFSET ?", (page_size, offset))
    data = cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM Products")
    total_records = cur.fetchone()[0]
    return data, total_records

# Function to update the table with the current page data
def update_table(tree, page, page_size):
    for i in tree.get_children():
        tree.delete(i)
    data, total_records = fetch_data(page, page_size)
    for row in data:
        tree.insert("", "end", values=row)
    return total_records

# Function to handle pagination
def change_page(tree, page, page_size, total_records, label):
    max_page = (total_records + page_size - 1) // page_size
    if page < 1:
        page = 1
    elif page > max_page:
        page = max_page
    total_records = update_table(tree, page, page_size)
    label.config(text=f"Page {page} of {max_page}")
    return page

def consult_inventory():
    sub_window = tk.Toplevel(config.window)
    sub_window.title("Consultar Estoque")

    # Define the page size
    page_size = 10
    current_page = 1

    # Create the Treeview widget
    columns = ("ID", "Nome", "Descrição", "Quantidade")
    tree = ttk.Treeview(sub_window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(expand=True, fill=tk.BOTH)

    # Create a label for pagination info
    pagination_label = tk.Label(sub_window, text="")
    pagination_label.pack(side=tk.TOP)

    # Create navigation buttons
    frame = tk.Frame(sub_window)
    frame.pack(side=tk.BOTTOM, fill=tk.X)

    def previous_page():
        nonlocal current_page
        current_page = change_page(tree, current_page - 1, page_size, total_records, pagination_label)

    def next_page():
        nonlocal current_page
        current_page = change_page(tree, current_page + 1, page_size, total_records, pagination_label)

    prev_button = tk.Button(frame, text="Previous", command=previous_page)
    prev_button.pack(side=tk.LEFT)

    next_button = tk.Button(frame, text="Next", command=next_page)
    next_button.pack(side=tk.RIGHT)

    # Initialize the table with the first page of data
    total_records = update_table(tree, current_page, page_size)
    change_page(tree, current_page, page_size, total_records, pagination_label)

def add_inventory():

    def to_uppercase(event):
        widget = event.widget
        text = widget.get()
        widget.delete(0, tk.END)
        widget.insert(0, text.upper())


    sub_window = tk.Toplevel(config.window)
    sub_window.title("Adicionar Estoque")

    # add labels for user input
    tk.Label(sub_window, text="Nome do produto:").grid(row=0, column=0, padx=10, pady=10)
    name_entry = tk.Entry(sub_window)
    name_entry.grid(row=0, column=1, padx=10, pady=10)
    name_entry.bind("<KeyRelease>", to_uppercase)

    tk.Label(sub_window, text="Descrição (opcional):").grid(row=1, column=0, padx=10, pady=10)
    description_entry = tk.Entry(sub_window)
    description_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(sub_window, text="Quantidade:").grid(row=2, column=0, padx=10, pady=10)
    amount_entry = tk.Entry(sub_window)
    amount_entry.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(sub_window, text="Preço:").grid(row=3, column=0, padx=10, pady=10)
    price_entry = tk.Entry(sub_window)
    price_entry.grid(row=3, column=1, padx=10, pady=10)

    def submit():
        name = name_entry.get().strip()
        description = description_entry.get().strip()
        amount = int(amount_entry.get().strip())
        price = float(price_entry.get().strip())

        if not name or not amount or not price:  # Check if mandatory fields are filled
            messagebox.showerror("Error", "Falta preencher campos obrigatórios")
            return

        cursor = config.db_connection.cursor()
        cursor.execute("INSERT INTO Products (Name, Description, Stock, Price) VALUES (?, ?, ?, ?)", (name, description, amount, round(price*100)))
        config.db_connection.commit()
        # Here you would add the code to insert the data into the database
        messagebox.showinfo("Success", "Produto adicionado com sucesso!")
        sub_window.destroy()

    submit_button = tk.Button(sub_window, text="Adicionar", command=submit)
    submit_button.grid(row=4, column=0, columnspan=2, pady=20)



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
    main_menu_commands["Estoque"]["Consultar Estoque"] = consult_inventory
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