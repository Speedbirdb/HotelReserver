import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import StringVar
#from scrapper import hotels_date, secondwindowstarter
#from workbenchgui import url

root = tk.Tk()
root.title("x")

root_width = root.winfo_width()
root_height = root.winfo_height()

def resize(event):
    screen_width = root.winfo_width()
    screen_height = root.winfo_height()

    blue_height = int(0.3 * screen_height)
    white_height = screen_height - blue_height

    blue_frame.place(relx=0, rely=0, relwidth=1, relheight=blue_height/screen_height)
    white_frame.place(relx=0, rely=blue_height/screen_height, relwidth=1, relheight=white_height/screen_height)

    bookingtext.place(relx=0.9, rely=blue_height/screen_height - 0.03, anchor="center")

blue_frame = tk.Frame(root, bg="#003B95")
white_frame = tk.Frame(root, bg="white")

# Create a new style for the "booking.TLabel"
styleofbookingcom = ttk.Style()
styleofbookingcom.configure("booking.TLabel", background="#003B95", foreground="white", font=("Segoe UI", 16, "bold"))

bookingtext = ttk.Label(root, text="booking.com", style="booking.TLabel")
bookingtext.place(relx=0.9, rely=0.3 - 0.03, anchor="center")

# Place blue and white frames
blue_frame.place(relx=0, rely=0, relwidth=1, relheight=0.3)
white_frame.place(relx=0, rely=0.3, relwidth=1, relheight=0.7)

root.state("zoomed")
root.mainloop()
