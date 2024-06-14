import tkinter as tk 
from PIL import Image, ImageTk
import os
import config
from . import widgets

def resize_image(image, max_width, max_height):
    # Calculate the scaling factor
    original_width, original_height = image.size
    ratio = min(max_width / original_width, max_height / original_height)
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)

    # Resize the image
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)

    # Create a new image with a transparent background
    new_image = Image.new("RGBA", (max_width, max_height), (0, 0, 0, 0))

    # Calculate the position to paste the resized image (centered)
    paste_x = (max_width - new_width) // 2
    paste_y = (max_height - new_height) // 2

    # Paste the resized image onto the new image
    new_image.paste(resized_image, (paste_x, paste_y), resized_image)

    return new_image


def create_image_button(img_path, toolbar, command=None, hoover_text=''):
    image = Image.open(img_path).convert("RGBA")
    image = resize_image(image, config.toolbar_size, config.toolbar_size)
    photo = ImageTk.PhotoImage(image)
    cmd = command if command is not None else lambda *args: None

    button = tk.Button(toolbar, image=photo, command=cmd)
    button.image = photo
    if len(hoover_text) > 0:
        button = widgets.add_hoover_text(button, config.window, hoover_text)

    return button

def add_toolbar():
    cwd = config.CWD # get global working directory
    window = config.window # get main window

    # Create a toolbar frame
    toolbar = tk.Frame(window, bd=1, relief=tk.RAISED)

    # Add buttons to the toolbar
    people_button = create_image_button(os.path.join(cwd, 'assets', 'couple-icon.png'), toolbar, hoover_text="Clientes")
    cart_button = create_image_button(os.path.join(cwd, 'assets', 'cart-black-icon.png'), toolbar, hoover_text="Compras")
    pen_button = create_image_button(os.path.join(cwd, 'assets', 'edit-pen-icon.png'), toolbar, hoover_text="Editar")
    download_button = create_image_button(os.path.join(cwd, 'assets', 'round-black-bottom-arrow-icon.png'), toolbar, hoover_text="Download")
    export_button = create_image_button(os.path.join(cwd, 'assets', 'document-export-icon.png'), toolbar)
    money_button = create_image_button(os.path.join(cwd, 'assets', 'money-bag-icon.png'), toolbar)


    # Pack the buttons into the toolbar
    people_button.pack(side=tk.LEFT, padx=2, pady=2)
    cart_button.pack(side=tk.LEFT, padx=2, pady=2)
    pen_button.pack(side=tk.LEFT, padx=2, pady=2)
    download_button.pack(side=tk.LEFT, padx=2, pady=2)
    export_button.pack(side=tk.LEFT, padx=2, pady=2)
    money_button.pack(side=tk.LEFT, padx=2, pady=2)

    # Pack the toolbar into the main window
    toolbar.pack(side=tk.TOP, fill=tk.X)
