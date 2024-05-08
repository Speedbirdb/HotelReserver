import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import StringVar
from tkinter import Scrollbar
from tkinter.ttk import OptionMenu  # Explicitly importing OptionMenu #first it did not recognized by the vscode
import tkcalendar as tkcal
from tkcalendar import Calendar
from datetime import date #getting date for blocking user to enter input before the current date
import requests

num1 = 0
num2 = 0

root = tk.Tk()

root.title("Booking.com")
base_url = "https://www.booking.com/searchresults.html?ss={}&ssne={}&ssne_untouched={}&efdco=1&label=gen173nr-1FCAEoggI46AdIM1gEaOQBiAEBmAExuAEHyAEP2AEB6AEBAECiAIBqAIDuAKo8sKxBsACAdICJGZlZWVmNGJjLWI2OGEtNGM0OS05ODk0LTM2ZGQ4YzkxYzY0MNgCBeACAQ&aid=304142&lang=en-us&sb=1&src_elem=sb&src=index&dest_id={}&dest_type=city&checkin={}&checkout={}&group_adults={}&no_rooms={}&group_children={}"

european_cities = [
    'London', 'Paris', 'Rome', 'Madrid', 'Berlin', 'Athens', 'Vienna', 'Warsaw', 'Amsterdam', 'Brussels',
    'Lisbon', 'Budapest', 'Prague', 'Barcelona', 'Milan', 'Munich', 'Hamburg', 'Istanbul', 'Zurich', 'Copenhagen',
    'Dublin', 'Oslo', 'Stockholm', 'Helsinki', 'Bratislava', 'Luxembourg', 'Geneva', 'Edinburgh', 'Venice',
    'Florence', 'Naples', 'Marseille', 'Nice', 'Strasbourg', 'Antwerp', 'Rotterdam', 'The Hague', 'Malaga',
    'Seville', 'Valencia', 'Bilbao', 'Lyon', 'Glasgow', 'Liverpool', 'Manchester', 'Birmingham', 'Leeds',
    'Cologne', 'Frankfurt', 'Dusseldorf', 'Hanover', 'Stuttgart', 'Dresden', 'Leipzig', 'Bremen', 'Essen',
    'Dortmund', 'Nuremberg', 'Lisbon', 'Porto', 'Braga', 'Faro', 'Coimbra', 'Aveiro', 'Viseu', 'Evora',
    'Setubal', 'Santarém', 'Cascais', 'Sintra', 'Albufeira', 'Funchal', 'Ponta Delgada', 'Angra do Heroísmo',
    'Horta', 'Bologna', 'Turin', 'Genoa', 'Verona', 'Padua', 'Trieste', 'Bari', 'Palermo', 'Catania',
    'Naples', 'Salerno', 'Cagliari', 'Olbia', 'Alghero', 'Sofia', 'Varna', 'Plovdiv', 'Burgas', 'Ruse'
]

# Function to adjust the layout based on window size
def on_resize(event):
    screen_width = root.winfo_width()
    screen_height = root.winfo_height()

    blue_height = int(0.3 * screen_height)
    white_height = screen_height - blue_height

    blue_frame.place(relx=0, rely=0, relwidth=1, relheight=blue_height/screen_height)
    white_frame.place(relx=0, rely=blue_height/screen_height, relwidth=1, relheight=white_height/screen_height)

    bookingtext.place(relx=0.9, rely=blue_height/screen_height - 0.03, anchor="center")

    upper_font_size = int(0.05 * screen_height)
    lower_font_size = int(0.02 * screen_height)

    styleforuppertext.configure("Upper.TLabel", font=("Blue Sans", upper_font_size, "bold"))
    styleforlowertext.configure("Lower.TLabel", font=("Segoe UI", lower_font_size, "italic"))

check_out_var = StringVar(root)
check_in_var = StringVar(root)

#these are added
def select_check_in_date():
    date = check_in_cal.get_date()
    check_in_var.set(date)
    attribute_transfer()
    return date #for the attribute_transfer method

def select_check_out_date():
    date = check_out_cal.get_date()
    check_out_var.set(date)
    attribute_transfer()
    return date # for the attribute_transfer method again

def select_city(event):
    selected_city.set(event)
    attribute_transfer()

def calendar_date_selected(event):
    if event.widget == check_in_cal:
        select_check_in_date()
    elif event.widget == check_out_cal:
        select_check_out_date()

def check_response_for_error():
    response = requests.get(url)
    
    if response.status_code == 200:
        print("Response is valid.")
    else:
        print("Error Code:", response.status_code)
        
        if response.status_code == 404:
            messagebox.showinfo("Error: The requested page was not found")
        elif response.status_code == 400:
            messagebox.showerror("Error: Bad request. Please check your input parameters.")
        elif response.status_code == 401:
            messagebox.showerror("Error: Unauthorized access. Please check your credentials.")
        elif response.status_code == 500:
            messagebox.showerror("Error: Internal server error. Please try again later.")
        else:
            messagebox.showerror("Error: An unknown error occurred.")

def attribute_transfer():
    global city, checkin_date, checkout_date
    if select_city and select_check_in_date() and select_check_out_date():
        if(select_check_in_date()<select_check_out_date()):
            #create messagebox
            messagebox.showinfo("Information", "Check-out date must be after check-in date.")
        elif(select_check_out_date()-select_check_in_date()).days >= 90:
            #create messagebox for over 90 nights
            messagebox.showinfo("Information", "Maximum stay duration is 90 nights.")
        else:
            city = selected_city.get()
            checkin_date = select_check_in_date()
            checkout_date = select_check_out_date()

            url = base_url.format(city, city, city, city, checkin_date, checkout_date, num_adults, num_rooms, num_children)
            check_response_for_error(url)


# Create blue and white frames
blue_frame = tk.Frame(root, bg="#003B95")
white_frame = tk.Frame(root, bg="white")

# Place blue and white frames
blue_frame.place(relx=0, rely=0, relwidth=1, relheight=0.3)
white_frame.place(relx=0, rely=0.3, relwidth=1, relheight=0.7)

def button_click_dropdown():
    variable = selected_city
    variable.set("Enter the city...")
    w = OptionMenu(root, variable, *european_cities, command=select_city)
    w.config(width=20)
    w.place(relx=0.2, rely=0.5, relwidth=0.2, relheight=0.1)
    scroll = Scrollbar(root, orient="vertical", command=w.yview)
    scroll.place(relx=0.4, rely=0.5, relheight=0.1, relwidth=0.01)
    w.config(yscrollcommand=scroll.set)
    w.bind("<FocusOut>", lambda event: w.place_forget())
    w.focus_set()

def toggle_calendar(calendar, placement_info, font_info):
    if calendar.winfo_ismapped():
        calendar.place_forget()
    else:
        calendar.place(relx=placement_info['relx'], rely=placement_info['rely'], relwidth=placement_info['relwidth'], relheight=placement_info['relheight'])
        calendar.config(font=font_info)

def create_calendar(relx, rely, relwidth, relheight, font):
    cal = Calendar(root, selectmode='day', year=2024, month=5, day=7)
    cal.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
    cal.config(font=font)

    current_date = date.today()
    for widget in cal.winfo_children():
        if isinstance(widget, tkcal.DateEntry):
            for date_entry in widget._calendar._dates:
                if date_entry < current_date:
                    widget._calendar._dates[date_entry].config(state='disabled')

    return cal


check_in_cal = None
check_out_cal = None

root_width = root.winfo_width()
root_height = root.winfo_height()

calendar_width = root_width * 0.2
calendar_height = calendar_width / 0.9

check_in_cal_placement_info = {'relx': 0.4, 'rely': 0.5, 'relwidth': calendar_width/root_width, 'relheight': calendar_height/root_height}
check_in_cal_font_info = ('Segoe UI', 8)

check_out_cal_placement_info = {'relx': 0.6, 'rely': 0.5, 'relwidth': calendar_width/root_width, 'relheight': calendar_height/root_height}
check_out_cal_font_info = ('Segoe UI', 8)

def calendar01sttimeornot():
    global num1
    global check_in_cal
    if num1 == 0:
        check_in_cal = create_calendar(**check_in_cal_placement_info, font=check_in_cal_font_info)
        num1 += 1
    else:
        if check_in_cal is not None:
            toggle_calendar(check_in_cal, check_in_cal_placement_info, check_in_cal_font_info)

def calendar21sttimeornot():
    global num2
    global check_out_cal
    if num2 == 0:
        check_out_cal = create_calendar(**check_out_cal_placement_info, font=check_out_cal_font_info)
        num2 += 1
    else:
        if check_out_cal is not None:
            toggle_calendar(check_out_cal, check_out_cal_placement_info, check_out_cal_font_info)


styleforuppertext = ttk.Style()
styleforlowertext = ttk.Style()
styleofbookingcom = ttk.Style()

# Initial font sizes for Upper and Lower text
initial_upper_font_size = 58
initial_lower_font_size = 20

styleforuppertext.configure("Upper.TLabel", background="#003B95", foreground="white")
styleforlowertext.configure("Lower.TLabel", background="#003B95", foreground="white")
styleofbookingcom.configure("booking.TLabel", background="#003B95", foreground="white", font=("Segoe UI", 16, "bold"))

selected_city = StringVar(root)

Upper_text = ttk.Label(root, text="Find your next stay", style="Upper.TLabel")
Upper_text.place(relx=0.2, rely=0.05, relwidth=0.4, relheight=0.1)
Lower_text = ttk.Label(root, text="Search deals on hotels and more", style="Lower.TLabel")
Lower_text.place(relx=0.2, rely=0.15, relwidth=0.6, relheight=0.1)
bookingtext = ttk.Label(root, text="booking.com", style="booking.TLabel")

# Create buttons
button1 = ttk.Button(root, text="Location", command=button_click_dropdown)
button1.place(relx=0.2, rely=0.4, relwidth=0.2, relheight=0.1)

button2 = ttk.Button(root, text="Check-In", command=calendar01sttimeornot)
button2.place(relx=0.4, rely=0.4, relwidth=0.2, relheight=0.1)

button3 = ttk.Button(root, text="Check-Out", command=calendar21sttimeornot)
button3.place(relx=0.6, rely=0.4, relwidth=0.2, relheight=0.1)

root.bind("<Configure>", on_resize)

root.mainloop()
