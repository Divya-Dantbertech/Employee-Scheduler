import tkinter as tk
from tkinter import ttk, messagebox
import csv
import random

# Function to categorize employees
def categorize_employees():
    sgt_cpl_employees = {}
    lcpl_pfc_pvt_employees = {}
    for employee in employee_availability:
        if employee.startswith(("SGT", "CPL")):
            sgt_cpl_employees[employee] = employee_availability[employee]
        elif employee.startswith(("LCPL", "PFC", "PVT")):
            lcpl_pfc_pvt_employees[employee] = employee_availability[employee]
    return sgt_cpl_employees, lcpl_pfc_pvt_employees

# Function to assign work days
def assign_work_days():
    sgt_cpl_employees, lcpl_pfc_pvt_employees = categorize_employees()
    
    try:
        work_days_sgt_cpl = list(map(int, sgt_cpl_days_entry.get().split(','))) if sgt_cpl_days_entry.get() else []
        work_days_lcpl_pfc_pvt = list(map(int, lcpl_pfc_pvt_days_entry.get().split(','))) if lcpl_pfc_pvt_days_entry.get() else []
    except ValueError:
        messagebox.showerror("Error", "Please enter valid comma-separated numbers for work days.")
        return [], []

    rotation_schedule_sgt_cpl = {employee: 0 for employee in sgt_cpl_employees}
    rotation_schedule_lcpl_pfc_pvt = {employee: 0 for employee in lcpl_pfc_pvt_employees}
    assigned_work_days_sgt_cpl = []
    assigned_work_days_lcpl_pfc_pvt = []

    for day in work_days_sgt_cpl:
        available_sgt_cpl = [employee for employee, unavailable_days in sgt_cpl_employees.items() if day not in unavailable_days and rotation_schedule_sgt_cpl[employee] < 1]
        if available_sgt_cpl:
            selected_employee = random.choice(available_sgt_cpl)
            assigned_work_days_sgt_cpl.append((day, selected_employee))
            rotation_schedule_sgt_cpl[selected_employee] += 1

    for day in work_days_lcpl_pfc_pvt:
        available_lcpl_pfc_pvt = [employee for employee, unavailable_days in lcpl_pfc_pvt_employees.items() if day not in unavailable_days and rotation_schedule_lcpl_pfc_pvt[employee] < 1]
        if available_lcpl_pfc_pvt:
            selected_employee = random.choice(available_lcpl_pfc_pvt)
            assigned_work_days_lcpl_pfc_pvt.append((day, selected_employee))
            rotation_schedule_lcpl_pfc_pvt[selected_employee] += 1

    return assigned_work_days_sgt_cpl, assigned_work_days_lcpl_pfc_pvt

# Function to save schedule to CSV
def save_schedule_to_csv():
    assigned_work_days_sgt_cpl, assigned_work_days_lcpl_pfc_pvt = assign_work_days()
   
    # Debugging print statements
    print("SGT/CPL:", assigned_work_days_sgt_cpl)
    print("LCPL/PFC/PVT:", assigned_work_days_lcpl_pfc_pvt)
    if not assigned_work_days_sgt_cpl and not assigned_work_days_lcpl_pfc_pvt:
        return
    
    with open('employee_schedule.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Category", "Day", "Employee"])
        for day, employee in assigned_work_days_sgt_cpl:
            writer.writerow(["SGT/CPL", day, employee])
        for day, employee in assigned_work_days_lcpl_pfc_pvt:
            writer.writerow(["LCPL/PFC/PVT", day, employee])
    messagebox.showinfo("Success", "Schedule saved to employee_schedule.csv")

# Function to display schedule
def display_schedule():
    assigned_work_days_sgt_cpl, assigned_work_days_lcpl_pfc_pvt = assign_work_days()
    if not assigned_work_days_sgt_cpl and not assigned_work_days_lcpl_pfc_pvt:
        return

    schedule_text.delete('1.0', tk.END)
    schedule_text.insert(tk.END, "SGT/CPL Employee Schedule:\n")
    for day, employee in assigned_work_days_sgt_cpl:
        schedule_text.insert(tk.END, f"Day {day}: {employee}\n")
    schedule_text.insert(tk.END, "\nLCPL/PFC/PVT Employee Schedule:\n")
    for day, employee in assigned_work_days_lcpl_pfc_pvt:
        schedule_text.insert(tk.END, f"Day {day}: {employee}\n")

# Function to add employee#f5 availability
def add_employee_availability():
    name = employee_name_entry.get()
    unavailable_days = unavailable_days_entry.get()
    if not name or not unavailable_days:
        messagebox.showerror("Error", "Please enter both employee name and unavailable days.")
        return
    try:
        unavailable_days = list(map(int, unavailable_days.split(',')))
    except ValueError:
        messagebox.showerror("Error", "Please enter valid comma-separated numbers for unavailable days.")
        return

    employee_availability[name] = unavailable_days
    employee_name_entry.delete(0, tk.END)
    unavailable_days_entry.delete(0, tk.END)
    messagebox.showinfo("Success", f"Added {name} with unavailable days {unavailable_days}")



# Set up the main Tkinter window
root = tk.Tk()
root.title("Employee Scheduler")
root.geometry("700x750")
root.resizable(width=False,height=False)


# Create a frame for the header
header_frame = tk.Frame(root, bg='black')  # Header background color
header_frame.grid(row=0, column=0, columnspan=2, pady=20, padx=10)

# Create and place the header label inside the frame
header_label = tk.Label(header_frame, text="Employee Scheduler", bg='#007BFF', fg='white', font=('Helvetica', 16, 'bold'))
header_label.pack(pady=10, padx=10)

# Set the background color of the root window
root.configure(bg="#C75B7A")  # Light gray background color

# Create a label with background color
label = tk.Label(root,
                 text="Employee Scheduler",
                 font=("Helvetica", 18, 'bold'),
                
                 fg='dark green',  # Text color
                 padx=29,  # Horizontal padding
                 pady=10)  # Vertical padding
label.grid(row=0, column=0, columnspan=2, pady=(10, 10), padx=120, sticky='ew')

 #Apply a style to the ttk widgets
style = ttk.Style(root)

#configure style for Labels
style.configure('TLabel',
                font=('Helvetica', 10, 'bold'),  # Modern font
                padding=4,  # Padding inside the label
                background='white',  # Light background color
                foreground='purple')  # Dark text color

# Configure the style for Buttons
style.configure('TButton',
                font=('Helvetica', 12, 'bold'),  # Modern font
                padding=10,  # Padding inside the button
                relief="flat",  # Flat relief for modern look
                background='#007BFF',  # Modern blue background color
                foreground='white')  # White text color

style.map('TButton',
          background=[('active', '#0056b3')],  # Darker shade on hover
          foreground=[('active', 'blue')])  # Keep text color white on hover

# Configure the style for Entry and Text
style.configure('TEntry',
                font=('Helvetica', 9),  # Modern font
                padding=6)  # Padding inside the entry

style.configure('TText',
                font=('Helvetica', 9),  # Modern font
                padding=6,  # Padding inside the text widget
                foreground='purple')  # Text color
                

# Initialize employee availability dictionary
employee_availability = {}

# Create and place widgets

def add_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(foreground='grey')

    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(foreground='black')

    def on_focus_out(event):
        if entry.get() == '':
            entry.insert(0, placeholder)
            entry.config(foreground='grey')

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)


ttk.Label(root, text="Employee Name").grid(row=1, column=0, pady=10, sticky='e',padx=(0, 30))
employee_name_entry = ttk.Entry(root, width=40)
employee_name_entry.grid(row=1, column=1, pady=8, sticky='w')
add_placeholder(employee_name_entry, "Enter employee name...")


ttk.Label(root, text="Unavailable Days (comma separated)").grid(row=2, column=0, pady=10, sticky='e',padx=(0, 15))
unavailable_days_entry = ttk.Entry(root, width=40)
unavailable_days_entry.grid(row=2, column=1, pady=8, sticky='w')
add_placeholder(unavailable_days_entry, "Enter your unavailable days....")


ttk.Label(root, text="SGT/CPL Work Days (comma separated)").grid(row=3, column=0, pady=10, sticky='e',padx=(0, 30))
sgt_cpl_days_entry = ttk.Entry(root, width=40)
sgt_cpl_days_entry.grid(row=3, column=1, pady=8, sticky='w')
add_placeholder(sgt_cpl_days_entry, "Enter work days as numbers, e.g., 1, 2, 15")


ttk.Label(root, text="LCPL/PFC/PVT Work Days (comma separated)").grid(row=4, column=0, pady=8, sticky='e',padx=(0, 15))
lcpl_pfc_pvt_days_entry = ttk.Entry(root, width=40)
lcpl_pfc_pvt_days_entry.grid(row=4, column=1, pady=8, sticky='w')
add_placeholder(lcpl_pfc_pvt_days_entry, "Enter work days as numbers, e.g., 3, 5, 20")


ttk.Button(root, text="Add Employee Availability", command=add_employee_availability).grid(row=6, column=0, pady=9, padx=(10,20), sticky='w')


# Apply a style to the ttk widgets
style = ttk.Style(root)

# Define a style for the button
style.configure('TButton',
                font=('Helvetica', 10, 'bold'),  # Modern font
                padding=3,  # Padding inside the button
                relief="flat",  # Flat relief for modern look
                background='red',  # Background color (Windows blue)
                foreground='purple')  # Text color
                
# Change the hover effect (optional)
style.map('TButton',
          background=[('active', 'yellow')],  # Darker shade on hover
          foreground=[('active', 'darkblue')])  # Keep the text color white

# Create a modern-looking button for "Generate Schedule"
generate_button = ttk.Button(root, text="Generate Schedule", style='TButton', command=display_schedule)
generate_button.grid(row=6, column=0, pady=9, padx=(240,0), sticky='e')

# Create a modern-looking button for "Save Schedule to CSV"
save_button = ttk.Button(root, text="Save Schedule to CSV", style='TButton', command=save_schedule_to_csv)
save_button.grid(row=6, column=1, pady=9, padx=(70,20), sticky='w')

schedule_text = tk.Text(root, wrap='word', width=70, height=15, font=('Helvetica', 11))
schedule_text.grid(row=7, column=0, columnspan=2, padx=(40,0), pady=10)

# Run the Tkinter main loop
root.mainloop()
