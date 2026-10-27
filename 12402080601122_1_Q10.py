import tkinter as tk
from tkinter import ttk, messagebox
import json
import csv
import os

FILE = "assignments.json"


def load_data():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []


data = load_data()


def save_data():
    # Save assignment data for later use
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


def clear():
    for entry in [enrollment, name, assignment, marks, remarks]:
        entry.delete(0, tk.END)
    status.set("Pending")


def show_data():
    # Refresh the table according to the selected filter
    for item in table.get_children():
        table.delete(item)

    selected = filter_status.get()

    for i, item in enumerate(data):
        if selected == "All" or item["status"] == selected:
            table.insert("", tk.END, iid=str(i), values=(
                item["enrollment"],
                item["name"],
                item["assignment"],
                item["status"],
                item["marks"],
                item["remarks"]
            ))


def add_data():
    e = enrollment.get().strip()
    n = name.get().strip()
    a = assignment.get().strip()
    m = marks.get().strip()
    r = remarks.get().strip()

    # Check required fields and marks
    if not e or not n or not a or not m:
        messagebox.showerror("Error", "Fill all required fields")
        return

    try:
        m = float(m)
    except:
        messagebox.showerror("Error", "Marks must be a number")
        return

    if m < 0:
        messagebox.showerror("Error", "Marks cannot be negative")
        return

    data.append({
        "enrollment": e,
        "name": n,
        "assignment": a,
        "status": status.get(),
        "marks": m,
        "remarks": r
    })

    save_data()
    show_data()
    clear()


def update_marks():
    selected = table.selection()

    if not selected:
        messagebox.showerror("Error", "Select an assignment")
        return

    try:
        m = float(marks.get())
    except:
        messagebox.showerror("Error", "Enter valid marks")
        return

    if m < 0:
        messagebox.showerror("Error", "Marks cannot be negative")
        return

    i = int(selected[0])
    data[i]["marks"] = m

    save_data()
    show_data()


def select_data(event):
    selected = table.selection()

    if not selected:
        return

    item = data[int(selected[0])]

    enrollment.delete(0, tk.END)
    enrollment.insert(0, item["enrollment"])

    name.delete(0, tk.END)
    name.insert(0, item["name"])

    assignment.delete(0, tk.END)
    assignment.insert(0, item["assignment"])

    status.set(item["status"])

    marks.delete(0, tk.END)
    marks.insert(0, item["marks"])

    remarks.delete(0, tk.END)
    remarks.insert(0, item["remarks"])


def export_csv():
    # Export all assignments into a CSV report
    with open("assignment_report.csv", "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            "Enrollment", "Name", "Assignment",
            "Status", "Marks", "Remarks"
        ])

        for item in data:
            writer.writerow([
                item["enrollment"],
                item["name"],
                item["assignment"],
                item["status"],
                item["marks"],
                item["remarks"]
            ])

    messagebox.showinfo("Success", "CSV file exported")


root = tk.Tk()
root.title("Assignment Tracker")
root.geometry("900x600")

tk.Label(root, text="Enrollment").grid(row=0, column=0, padx=5, pady=5)
enrollment = tk.Entry(root)
enrollment.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Name").grid(row=0, column=2, padx=5, pady=5)
name = tk.Entry(root)
name.grid(row=0, column=3, padx=5, pady=5)

tk.Label(root, text="Assignment").grid(row=1, column=0, padx=5, pady=5)
assignment = tk.Entry(root)
assignment.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Status").grid(row=1, column=2, padx=5, pady=5)
status = ttk.Combobox(
    root,
    values=["Pending", "Completed"],
    state="readonly"
)
status.set("Pending")
status.grid(row=1, column=3, padx=5, pady=5)

tk.Label(root, text="Marks").grid(row=2, column=0, padx=5, pady=5)
marks = tk.Entry(root)
marks.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Remarks").grid(row=2, column=2, padx=5, pady=5)
remarks = tk.Entry(root)
remarks.grid(row=2, column=3, padx=5, pady=5)

tk.Button(root, text="Add", command=add_data).grid(row=3, column=0, pady=10)
tk.Button(root, text="Update Marks", command=update_marks).grid(row=3, column=1)
tk.Button(root, text="Export CSV", command=export_csv).grid(row=3, column=2)
tk.Button(root, text="Clear", command=clear).grid(row=3, column=3)

tk.Label(root, text="Filter").grid(row=4, column=0, padx=5, pady=5)

filter_status = ttk.Combobox(
    root,
    values=["All", "Pending", "Completed"],
    state="readonly"
)
filter_status.set("All")
filter_status.grid(row=4, column=1)
filter_status.bind("<<ComboboxSelected>>", lambda e: show_data())

columns = [
    "Enrollment",
    "Name",
    "Assignment",
    "Status",
    "Marks",
    "Remarks"
]

table = ttk.Treeview(
    root,
    columns=columns,
    show="headings"
)

# Create the table headings
for column in columns:
    table.heading(column, text=column)
    table.column(column, width=130)

table.grid(row=5, column=0, columnspan=4, padx=10, pady=10)
table.bind("<<TreeviewSelect>>", select_data)

show_data()

root.mainloop()
