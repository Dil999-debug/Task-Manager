import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

CSV_FILE = "tasks.csv"


def create_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["TaskID", "TaskName", "Status", "TimeTaken"])


def add_task():
    task_id = entry_id.get()
    task_name = entry_name.get()
    status = status_var.get()
    time_taken = entry_time.get()

    if task_id == "" or task_name == "" or time_taken == "":
        messagebox.showerror("Error", "Please fill all fields")
        return

    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([task_id, task_name, status, time_taken])

    messagebox.showinfo("Success", "Task Added Successfully")

    clear_fields()
    view_tasks()
    productivity_analysis()


def view_tasks():
    for row in tree.get_children():
        tree.delete(row)

    with open(CSV_FILE, mode='r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            tree.insert('', tk.END, values=row)


def delete_task():
    selected_item = tree.selection()

    if not selected_item:
        messagebox.showerror("Error", "Please select a task")
        return

    values = tree.item(selected_item)['values']
    task_id = values[0]

    tasks = []

    with open(CSV_FILE, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)

        for row in reader:
            if row[0] != str(task_id):
                tasks.append(row)

    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(tasks)

    messagebox.showinfo("Success", "Task Deleted Successfully")

    view_tasks()
    productivity_analysis()


def update_task():
    selected_item = tree.selection()

    if not selected_item:
        messagebox.showerror("Error", "Please select a task")
        return

    new_status = update_status_var.get()

    values = tree.item(selected_item)['values']
    task_id = values[0]

    tasks = []

    with open(CSV_FILE, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)

        for row in reader:
            if row[0] == str(task_id):
                row[2] = new_status
            tasks.append(row)

    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(tasks)

    messagebox.showinfo("Success", "Task Updated Successfully")

    view_tasks()
    productivity_analysis()


def productivity_analysis():
    total_tasks = 0
    completed_tasks = 0
    pending_tasks = 0
    total_time = 0

    with open(CSV_FILE, mode='r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            total_tasks += 1

            if row[2] == "Completed":
                completed_tasks += 1
            else:
                pending_tasks += 1

            total_time += int(row[3])

    if total_tasks > 0:
        productivity = (completed_tasks / total_tasks) * 100
        average_time = total_time / total_tasks
    else:
        productivity = 0
        average_time = 0

    label_completed.config(text=f"Completed Tasks: {completed_tasks}")
    label_pending.config(text=f"Pending Tasks: {pending_tasks}")
    label_productivity.config(text=f"Productivity: {productivity:.2f}%")
    label_average.config(text=f"Average Time: {average_time:.2f} min")


def export_report():
    total_tasks = 0
    completed_tasks = 0
    pending_tasks = 0
    total_time = 0

    with open(CSV_FILE, mode='r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            total_tasks += 1

            if row[2] == "Completed":
                completed_tasks += 1
            else:
                pending_tasks += 1

            total_time += int(row[3])

    if total_tasks > 0:
        productivity = (completed_tasks / total_tasks) * 100
        average_time = total_time / total_tasks
    else:
        productivity = 0
        average_time = 0

    with open("productivity_report.txt", mode='w') as file:
        file.write("PRODUCTIVITY REPORT\n")
        file.write("========================\n")
        file.write(f"Total Tasks: {total_tasks}\n")
        file.write(f"Completed Tasks: {completed_tasks}\n")
        file.write(f"Pending Tasks: {pending_tasks}\n")
        file.write(f"Productivity Percentage: {productivity:.2f}%\n")
        file.write(f"Average Time Per Task: {average_time:.2f} minutes\n")

    messagebox.showinfo("Success", "Report Exported Successfully")


def clear_fields():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_time.delete(0, tk.END)


root = tk.Tk()
root.title("Task Management Dashboard")
root.geometry("1000x700")
root.config(bg="#081b3a")

create_csv()

title = tk.Label(
    root,
    text="Task Management Dashboard",
    font=("Arial", 22, "bold"),
    bg="#081b3a",
    fg="white"
)

title.pack(pady=10)

input_frame = tk.Frame(root, bg="#081b3a")
input_frame.pack(pady=10)

tk.Label(input_frame, text="Task ID", bg="#081b3a", fg="white").grid(row=0, column=0, padx=10)
entry_id = tk.Entry(input_frame)
entry_id.grid(row=0, column=1, padx=10)

tk.Label(input_frame, text="Task Name", bg="#081b3a", fg="white").grid(row=0, column=2, padx=10)
entry_name = tk.Entry(input_frame)
entry_name.grid(row=0, column=3, padx=10)

tk.Label(input_frame, text="Status", bg="#081b3a", fg="white").grid(row=1, column=0, padx=10)

status_var = tk.StringVar()
status_var.set("Pending")

status_menu = ttk.Combobox(
    input_frame,
    textvariable=status_var,
    values=["Completed", "Pending"],
    state="readonly"
)
status_menu.grid(row=1, column=1, padx=10)

tk.Label(input_frame, text="Time Taken (min)", bg="#081b3a", fg="white").grid(row=1, column=2, padx=10)
entry_time = tk.Entry(input_frame)
entry_time.grid(row=1, column=3, padx=10)

button_frame = tk.Frame(root, bg="#081b3a")
button_frame.pack(pady=10)

btn_add = tk.Button(
    button_frame,
    text="Add Task",
    bg="#0d6efd",
    fg="white",
    width=15,
    command=add_task
)
btn_add.grid(row=0, column=0, padx=10)

btn_delete = tk.Button(
    button_frame,
    text="Delete Task",
    bg="#dc3545",
    fg="white",
    width=15,
    command=delete_task
)
btn_delete.grid(row=0, column=1, padx=10)

update_status_var = tk.StringVar()
update_status_var.set("Completed")

update_menu = ttk.Combobox(
    button_frame,
    textvariable=update_status_var,
    values=["Completed", "Pending"],
    state="readonly",
    width=12
)
update_menu.grid(row=0, column=2, padx=10)

btn_update = tk.Button(
    button_frame,
    text="Update Task",
    bg="#198754",
    fg="white",
    width=15,
    command=update_task
)
btn_update.grid(row=0, column=3, padx=10)

btn_export = tk.Button(
    button_frame,
    text="Export Report",
    bg="#ffc107",
    fg="black",
    width=15,
    command=export_report
)
btn_export.grid(row=0, column=4, padx=10)

tree_frame = tk.Frame(root)
tree_frame.pack(pady=20)

columns = ("TaskID", "TaskName", "Status", "TimeTaken")

tree = ttk.Treeview(
    tree_frame,
    columns=columns,
    show='headings',
    height=10
)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=180)

tree.pack()

analysis_frame = tk.Frame(root, bg="#081b3a")
analysis_frame.pack(pady=20)

label_completed = tk.Label(
    analysis_frame,
    text="Completed Tasks: 0",
    font=("Arial", 12, "bold"),
    bg="#081b3a",
    fg="lightgreen"
)
label_completed.pack(pady=5)

label_pending = tk.Label(
    analysis_frame,
    text="Pending Tasks: 0",
    font=("Arial", 12, "bold"),
    bg="#081b3a",
    fg="orange"
)
label_pending.pack(pady=5)

label_productivity = tk.Label(
    analysis_frame,
    text="Productivity: 0%",
    font=("Arial", 12, "bold"),
    bg="#081b3a",
    fg="cyan"
)
label_productivity.pack(pady=5)

label_average = tk.Label(
    analysis_frame,
    text="Average Time: 0 min",
    font=("Arial", 12, "bold"),
    bg="#081b3a",
    fg="white"
)
label_average.pack(pady=5)

view_tasks()
productivity_analysis()

root.mainloop()