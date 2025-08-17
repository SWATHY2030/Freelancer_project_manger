from tkinter import *
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import csv
import Freelance_database 

# Connect to database 
Freelance_database.connect_db()

root = Tk()
root.title("Freelance Project Manager")
root.geometry("1000x650")
root.resizable(False, False)

#colors and fonts
BG_COLOR = "#f0f2f5"
PRIMARY_COLOR = "purple"
SECONDARY_COLOR = "purple"
ACCENT_COLOR = "#fd79a8"
TEXT_COLOR = "#2d3436"
FONT_PRIMARY = ("Segoe UI", 14)
FONT_SECONDARY = ("Segoe UI", 12)
FONT_TITLE = ("Segoe UI", 18, "bold")

# Set background color
root.config(bg=BG_COLOR)



# Variables
client_var = StringVar()
title_var = StringVar()
fee_var = StringVar()
deadline_var = StringVar()
status_var = StringVar()
search_var = StringVar()
status_var.set("pending")

#Functions
def add_project():
    if client_var.get() == "" or title_var.get() == "":
        messagebox.showerror("Error", "All fields are required")
        return
    Freelance_database.insert_project(client_var.get(), title_var.get(), fee_var.get(), deadline_var.get(), status_var.get())
    messagebox.showinfo("Success", "Project added successfully")
    show_projects()
    update_status_bar()
    clear_form()
    

def show_projects():
    for i in table.get_children():
        table.delete(i)
    rows = Freelance_database.fetch_all()
    for row in rows:
        table.insert("", END, values=row)
    update_status_bar()

def clear_form():
    client_var.set("")
    title_var.set("")
    fee_var.set("")
    deadline_var.set("")
    status_var.set("Pending")

def search_projects():
    for i in table.get_children():
        table.delete(i)
    rows = Freelance_database.search_projects(search_var.get())
    for row in rows:
        table.insert("", END, values=row)
    update_status_bar()
def delete_selected():
    selected = table.focus()
    if not selected:
        messagebox.showwarning("Select", "Please select a project")
        return
    project_id = table.item(selected)['values'][0]
    Freelance_database.delete_project(project_id)
    show_projects()
    update_status_bar()

def calculate_income():
    total = 0
    for row in Freelance_database.fetch_all():
        if datetime.strptime(str(row[4]), "%Y-%m-%d").month == datetime.now().month:
            total += float(row[3])
    messagebox.showinfo("Monthly Income", f"Total: ₹{total:.2f}")

def export_to_csv():
    rows = Freelance_database.fetch_all()
    if not rows:
        messagebox.showwarning("No Data", "No projects to export.")
        return
    file = filedialog.asksaveasfilename(defaultextension=".csv",
                                      filetypes=[("CSV files", "*.csv")],
                                      title="Save As")
    if file:
        try:
            with open(file, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Client Name", "Project Title", "Fee", "Deadline", "Status"])
                for row in rows:
                    writer.writerow(row)
            messagebox.showinfo("Success", f"Exported to:\n{file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export:\n{e}")
def update_status_bar():
    total_projects = len(table.get_children())
    status_label.config(text=f"Total Projects: {total_projects}")

    
   

# Main Title
title_frame = Frame(root, bg=PRIMARY_COLOR)
title_frame.pack(fill=X, padx=10, pady=10)

Label(title_frame, text="FREELANCER PROJECT LIST", font=FONT_TITLE, 
      bg=PRIMARY_COLOR, fg="white").pack(pady=10)

#Main Content Frame
main_frame = Frame(root, bg=BG_COLOR)
main_frame.pack(fill=BOTH, expand=True, padx=10, pady=(0, 10))

# Form Frame 
form_frame = Frame(main_frame, bg="white", bd=0, relief=RIDGE, 
                  highlightbackground=SECONDARY_COLOR, highlightthickness=2)
form_frame.pack(side=LEFT, fill=Y, padx=(0, 10))

form_header = Frame(form_frame, bg=PRIMARY_COLOR)
form_header.pack(fill=X)
Label(form_header, text="Project Details", font=FONT_PRIMARY, 
      bg=PRIMARY_COLOR, fg="white", padx=10, pady=5).pack()

form_content = Frame(form_frame, bg="white", padx=20, pady=20)
form_content.pack(fill=BOTH, expand=True)

# Form Fields
Label(form_content, text="Client Name", bg="white",font=FONT_SECONDARY, fg=TEXT_COLOR ).grid(row=0, column=0, sticky=W, pady=5)
Entry(form_content, textvariable=client_var, font=FONT_SECONDARY,bd=1, relief=SOLID, highlightcolor=PRIMARY_COLOR).grid(row=0, column=1, pady=5, padx=10)

Label(form_content, text="Project Title", bg="white",font=FONT_SECONDARY, fg=TEXT_COLOR).grid(row=1, column=0, sticky=W, pady=5)
Entry(form_content, textvariable=title_var, font=FONT_SECONDARY,bd=1, relief=SOLID).grid(row=1, column=1, pady=5, padx=10)

Label(form_content, text="Fee (₹)", bg="white",font=FONT_SECONDARY, fg=TEXT_COLOR).grid(row=2, column=0, sticky=W, pady=5)
Entry(form_content, textvariable=fee_var, font=FONT_SECONDARY, bd=1, relief=SOLID).grid(row=2, column=1, pady=5, padx=10)

Label(form_content, text="Deadline", bg="white",font=FONT_SECONDARY, fg=TEXT_COLOR).grid(row=3, column=0, sticky=W, pady=5)
Entry(form_content, textvariable=deadline_var, font=FONT_SECONDARY,bd=1, relief=SOLID).grid(row=3, column=1, pady=5, padx=10)

Label(form_content, text="Status", bg="white",font=FONT_SECONDARY, fg=TEXT_COLOR).grid(row=4, column=0, sticky=W, pady=5)
ttk.Combobox(form_content, textvariable=status_var,values=["Pending", "Completed", "In Progress"],font=FONT_SECONDARY, state="readonly").grid(row=4, column=1, pady=5, padx=10)

# Form Buttons
button_frame = Frame(form_content, bg="white")
button_frame.grid(row=5, column=0, columnspan=2, pady=15)

Button(button_frame, text="Add Project", command=add_project,bg=PRIMARY_COLOR, fg="white", font=FONT_SECONDARY, bd=0, padx=15, pady=5).pack(side=LEFT, padx=5)
Button(button_frame, text="Clear", command=clear_form,bg=SECONDARY_COLOR, fg="white", font=FONT_SECONDARY, bd=0, padx=15, pady=5).pack(side=LEFT, padx=5)
Button(button_frame, text="Delete", command=delete_selected,bg=ACCENT_COLOR, fg="white", font=FONT_SECONDARY, bd=0, padx=15, pady=5).pack(side=LEFT, padx=5)

#Right Panel
right_frame = Frame(main_frame, bg=BG_COLOR)
right_frame.pack(side=LEFT, fill=BOTH, expand=True)

# Search Bar
search_frame = Frame(right_frame, bg=BG_COLOR)
search_frame.pack(fill=X, pady=(0, 10))

Entry(search_frame, textvariable=search_var, font=FONT_SECONDARY,bd=1, relief=SOLID).pack(side=LEFT, fill=X, expand=True, padx=(0, 5))
Button(search_frame, text="Search", command=search_projects,bg=PRIMARY_COLOR, fg="white", font=FONT_SECONDARY, bd=0).pack(side=LEFT, padx=(0, 5))
Button(search_frame, text="Show All", command=show_projects, bg=SECONDARY_COLOR, fg="white", font=FONT_SECONDARY, bd=0).pack(side=LEFT, padx=(0, 5))
Button(search_frame, text="Export CSV", command=export_to_csv,bg="#00b894", fg="white", font=FONT_SECONDARY, bd=0).pack(side=LEFT, padx=(0, 5))
Button(search_frame, text="Income", command=calculate_income,bg="#e17055", fg="white", font=FONT_SECONDARY, bd=0).pack(side=LEFT)

# Table Frame
table_frame = Frame(right_frame, bg="white", bd=0, relief=RIDGE,highlightbackground=SECONDARY_COLOR, highlightthickness=2)
table_frame.pack(fill=BOTH, expand=True)

# Add scrollbars
scroll_y = Scrollbar(table_frame, orient=VERTICAL)
scroll_y.pack(side=RIGHT, fill=Y)

scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
scroll_x.pack(side=BOTTOM, fill=X)

# Create table
table = ttk.Treeview(table_frame, columns=("ID", "Client", "Title", "Fee", "Deadline", "Status"),show="headings", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

scroll_y.config(command=table.yview)
scroll_x.config(command=table.xview)

table.pack(fill=BOTH, expand=True)

# Configure columns
table.heading("ID", text="ID", anchor=CENTER)
table.heading("Client", text="Client", anchor=CENTER)
table.heading("Title", text="Title", anchor=CENTER)
table.heading("Fee", text="Fee (₹)", anchor=CENTER)
table.heading("Deadline", text="Deadline", anchor=CENTER)
table.heading("Status", text="Status", anchor=CENTER)

table.column("ID", width=40, anchor=CENTER)
table.column("Client", width=120, anchor=CENTER)
table.column("Title", width=150, anchor=CENTER)
table.column("Fee", width=80, anchor=CENTER)
table.column("Deadline", width=100, anchor=CENTER)
table.column("Status", width=100, anchor=CENTER)

# Style the table
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="white", fieldbackground="white",foreground=TEXT_COLOR, font=FONT_SECONDARY)
style.configure("Treeview.Heading", background=PRIMARY_COLOR,foreground="white", font=FONT_SECONDARY)
style.map("Treeview", background=[('selected', SECONDARY_COLOR)])

# Status bar
status_frame = Frame(root, bg=PRIMARY_COLOR, height=30)
status_frame.pack(fill=X, padx=10, pady=(0, 10))
status_label = Label(status_frame, text="Total Projects: 0", bg=PRIMARY_COLOR, fg="white", font=FONT_SECONDARY)
status_label.pack(side=LEFT, padx=10)

# Initial load
show_projects()
update_status_bar()  
root.mainloop()
