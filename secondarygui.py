import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import StringVar
import pandas as pd

try:
    df = pd.read_csv('hotel_data.csv')
except FileNotFoundError:
    messagebox.showerror("Error", "CSV file not found!")
    exit()

root = tk.Tk()
root.title("Booking.com/SearchResults")

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
df['price_TRY'] = df['price_TRY'].str.replace('TL', '').str.replace(',', '').astype(int)
original_df = df.copy()

divide_flag = False

def update_prices():
    global df, original_df, divide_flag
    if divide_flag:
        df['price_TRY'] = original_df['price_TRY']
        tree.heading("price_TRY", text="price_TRY")
    else:
        df['price_TRY'] = original_df['price_TRY'] // 30
        tree.heading("price_TRY", text="price_EUR")
    divide_flag = not divide_flag
    refresh_treeview()

def refresh_treeview():
    tree.delete(*tree.get_children())
    for _, row in df.iterrows():
        tree.insert("", "end", values=row.tolist())

styleofbookingcom = ttk.Style()
styleofbookingcom.configure("booking.TLabel", background="#003B95", foreground="white", font=("Segoe UI", 16, "bold"))

bookingtext = ttk.Label(root, text="booking.com", style="booking.TLabel")
bookingtext.place(relx=0.9, rely=0.3 - 0.03, anchor="center")

blue_frame.place(relx=0, rely=0, relwidth=1, relheight=0.3)
white_frame.place(relx=0, rely=0.3, relwidth=1, relheight=0.7)

df.sort_values("price_TRY", axis=0, ascending=True, inplace=True, na_position='first')

style = ttk.Style()
style.configure("My.Treeview", font=('Segoe UI', 9), background='white', foreground='black')
style.configure("My.Treeview.Heading", font=('Segoe UI', 12, 'bold'), background='grey', foreground='black')

tree = ttk.Treeview(white_frame, style="My.Treeview")
columns = list(df.columns) 
tree["columns"] = columns
for col in columns:
    print(col)
    if col == "price_TRY":
        tree.heading(col, text="price_TRY", command=update_prices)
    else:
        tree.heading(col, text=col, anchor=tk.W)
for _, row in df.iterrows():  
    tree.insert("", "end", values=row.tolist())

tree.pack(fill="both", expand=True)

root.state("zoomed")
root.mainloop()
