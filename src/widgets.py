import tkinter as tk
from PIL import Image, ImageTk

def create_transparent_image(color, alpha, width, height):
    image = Image.new("RGBA", (width, height), color)
    for x in range(width):
        for y in range(height):
            image.putpixel((x, y), (*image.getpixel((x, y))[:3], alpha))
    return ImageTk.PhotoImage(image)

def add_hoover_text(button, window, text, time_to_display=1):
    # Add hoover text to a button 

    timer_id = None
    cursor_x = 0
    cursor_y = 0
    cursor_check_id = None

    # updates cursor position
    def store_cursor_position(event):
        nonlocal cursor_x, cursor_y
        cursor_x = event.x_root - window.winfo_rootx()
        cursor_y = event.y_root - window.winfo_rooty()
        if not (0 <= event.x <= button.winfo_width() and 0 <= event.y <= button.winfo_height()):
            hide_info()

    # shows info_label
    def show_info():
        nonlocal cursor_x, cursor_y
        info_label.place(x=cursor_x + 10,
                         y=cursor_y + 10)
        start_checking_cursor_position()

    # schedules showing info_label
    def schedule_show_info(event):
        nonlocal timer_id
        timer_id = window.after(time_to_display*1000, show_info)  # Schedule show_info to be called

    # cancels showing info_label
    def cancel_show_info(event):
        nonlocal timer_id
        if timer_id is not None:
            window.after_cancel(timer_id)
            timer_id = None
        if not (0 <= event.x <= button.winfo_width() and 0 <= event.y <= button.winfo_height()):
            hide_info()

    # monitor cursor position
    def start_checking_cursor_position():
        nonlocal cursor_check_id
        cursor_check_id = window.after(100, check_cursor_position)

    # if cursor slipped away remove text
    def check_cursor_position():
        nonlocal cursor_check_id, button
        if not (button.winfo_rootx() <= window.winfo_pointerx() <= button.winfo_rootx() + button.winfo_width() and
                button.winfo_rooty() <= window.winfo_pointery() <= button.winfo_rooty() + button.winfo_height()):
            hide_info()
        else:
            cursor_check_id = window.after(100, check_cursor_position)

    def hide_info():
        nonlocal cursor_check_id
        info_label.place_forget()
        if cursor_check_id is not None:
            window.after_cancel(cursor_check_id)
            cursor_check_id = None

    info_label = tk.Label(window, text=text, bg="#ece8b4", relief=tk.SOLID)
    info_label.place_forget()  # Hide initially

    button.bind("<Enter>", schedule_show_info)
    button.bind("<Motion>", store_cursor_position)  # Update cursor position as it moves over the button
    button.bind("<Leave>", cancel_show_info)
    return button
