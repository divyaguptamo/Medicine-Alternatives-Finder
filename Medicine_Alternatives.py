import tkinter as tk
from tkinter import messagebox, StringVar, Entry, Checkbutton, IntVar, Frame
import csv

# Function to load medicine data from CSV file
def load_medicine_data(filename):
    medicine_db = {}
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = row["Medicine"].strip() if "Medicine" in row else row["Component"].strip()
            if key not in medicine_db:
                medicine_db[key] = []
            medicine_db[key].append({
                "component": row["Component"],
                "alternative": row["Alternative"],
                "price": int(row['Price'])
            })
    return medicine_db

# Function to open the search window
def search_window(csv_file, title):
    global search_root, selected_medicine
    medicine_db = load_medicine_data(csv_file)
    medicine_list = sorted(medicine_db.keys())
    
    def find_alternative():
        if selected_medicine.get():
            alternatives = sorted(medicine_db[selected_medicine.get()], key=lambda x: x["price"])
            result_text = "\n".join([f"{alt['alternative']} - ₹{alt['price']}" for alt in alternatives])
            result_label.config(text=result_text)
        else:
            messagebox.showerror("Error", "No medicine selected")
    
    def go_back():
        search_root.destroy()
        show_options()
    
    def update_suggestions(event):
        typed_text = entry_var.get().strip().lower()
        for cb in checkbuttons:
            cb.pack_forget()
        checkbuttons.clear()
        if typed_text:
            filtered_meds = [med for med in medicine_list if typed_text in med.lower()]
            for med in filtered_meds:
                cb = Checkbutton(suggestion_frame, text=med, variable=selected_medicine, onvalue=med, offvalue="")
                cb.pack(anchor='w')
                checkbuttons.append(cb)
    
    search_root = tk.Toplevel()
    search_root.title(title)
    search_root.geometry("400x400")
    
    tk.Label(search_root, text=title, font=("Arial", 12, "bold")).pack(pady=10)
    entry_var = StringVar()
    entry = Entry(search_root, textvariable=entry_var)
    entry.pack(pady=5)
    entry.bind("<KeyRelease>", update_suggestions)
    
    suggestion_frame = Frame(search_root)
    suggestion_frame.pack(pady=5)
    
    checkbuttons = []
    selected_medicine = StringVar()
    
    search_button = tk.Button(search_root, text="Find Alternative", command=find_alternative)
    search_button.pack(pady=10)
    
    result_label = tk.Label(search_root, text="", fg="blue", font=("Arial", 12))
    result_label.pack(pady=10)
    
    back_button = tk.Button(search_root, text="Back", command=go_back)
    back_button.pack(pady=10)
    
    search_root.mainloop()

# Function to show options page
def show_options():
    global options_root
    options_root = tk.Toplevel()
    options_root.title("Options")
    options_root.geometry("400x300")
    
    search_by_name_button = tk.Button(options_root, text="Search by Medicine Name", command=lambda: [options_root.destroy(), search_window("medicine_data3.csv", "Select Medicine Name")], width=25)
    search_by_composition_button = tk.Button(options_root, text="Search by Composition", command=lambda: [options_root.destroy(), search_window("medicine_data2.csv", "Select Composition")], width=25)
    
    search_by_name_button.pack(pady=10)
    search_by_composition_button.pack(pady=10)
    
    options_root.mainloop()

# Main Menu Window
def main_menu():
    global root
    root = tk.Tk()
    root.title("Indian Medical AI")
    root.geometry("400x300")
    
    tk.Label(root, text="Indian Medical AI", font=("Arial", 14, "bold")).pack(pady=20)
    
    start_button = tk.Button(root, text="Get Started", command=show_options, width=25)
    start_button.pack(pady=10)
    
    root.mainloop()

# Start the application
main_menu()
