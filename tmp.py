import tkinter as tk
from tkinter import ttk

def setup_treeview(parent):
    # Define columns
    columns = ("ProductID", "Name", "Description", "Stock", "Price")
    
    # Create Treeview
    treeview = ttk.Treeview(parent, columns=columns, show="headings", style="Custom.Treeview")
    
    # Define headings and column properties
    treeview.heading("ProductID", text="Product ID")
    treeview.heading("Name", text="Name")
    treeview.heading("Description", text="Description")
    treeview.heading("Stock", text="Stock")
    treeview.heading("Price", text="Price")

    treeview.column("ProductID", width=100, anchor="center")
    treeview.column("Name", width=150, anchor="center")
    treeview.column("Description", width=250, anchor="center")
    treeview.column("Stock", width=100, anchor="center")
    treeview.column("Price", width=100, anchor="center")

    # Add vertical and horizontal scrollbars
    vsb = ttk.Scrollbar(parent, orient="vertical", command=treeview.yview)
    hsb = ttk.Scrollbar(parent, orient="horizontal", command=treeview.xview)
    treeview.configure(yscroll=vsb.set, xscroll=hsb.set)
    
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")
    treeview.grid(row=0, column=0, sticky="nsew")

    return treeview

def populate_treeview(treeview, data):
    # Clear existing data
    for row in treeview.get_children():
        treeview.delete(row)

    # Insert new data
    for item in data:
        treeview.insert("", "end", values=item)

# Example usage
def main():
    root = tk.Tk()
    root.title("Product List")
    root.geometry("700x400")

    # Configure grid layout
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Style the Treeview for grid-like appearance
    style = ttk.Style()
    style.configure("Custom.Treeview", 
                    rowheight=25, 
                    borderwidth=1, 
                    relief="solid")
    style.configure("Custom.Treeview.Heading", 
                    font=("Helvetica", 10, "bold"), 
                    borderwidth=1, 
                    relief="solid")
    style.layout("Custom.Treeview.Heading", [
        ("Custom.Treeview.Heading.cell", {"sticky": "nswe"}),
        ("Custom.Treeview.Heading.image", {"side": "right", "sticky": ""}),
        ("Custom.Treeview.Heading.text", {"sticky": "we"})
    ])

    # Setup Treeview
    treeview = setup_treeview(root)

    # Sample data
    data = [
        (1, "Product A", "Description of product A", 10, 100),
        (2, "Product B", "Description of product B", 15, 150),
        (3, "Product C", "Description of product C", 20, 200),
    ]

    # Populate Treeview
    populate_treeview(treeview, data)

    root.mainloop()

if __name__ == "__main__":
    main()
