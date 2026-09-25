import tkinter as tk
from tkinter import messagebox
import json
import os


FILE_NAME = "tasks.json"

# Store tasks
tasks = []


# =========================================================
# LOAD TASKS
# =========================================================

def load_tasks():
    global tasks

    if not os.path.exists(FILE_NAME):
        tasks = []
        return

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            tasks = data
        else:
            tasks = []

    except (json.JSONDecodeError, OSError):
        tasks = []

    # Make sure data is correct
    fixed_tasks = []

    for task in tasks:

        if isinstance(task, dict):
            fixed_tasks.append({
                "text": str(task.get("text", "")),
                "completed": bool(task.get("completed", False))
            })

        elif isinstance(task, str):

            completed = task.startswith("✓ ")

            if completed:
                task = task[2:]

            fixed_tasks.append({
                "text": task,
                "completed": completed
            })

    tasks = fixed_tasks


# =========================================================
# SAVE TASKS
# =========================================================

def save_tasks():

    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4, ensure_ascii=False)

    except OSError:
        messagebox.showerror(
            "Error",
            "Could not save tasks."
        )


# =========================================================
# REFRESH TASK LIST
# =========================================================

def refresh_tasks():

    task_list.delete(0, tk.END)

    for task in tasks:

        if task["completed"]:
            text = "✓ " + task["text"]
        else:
            text = "○ " + task["text"]

        task_list.insert(tk.END, text)

    update_counter()


# =========================================================
# ADD TASK
# =========================================================

def add_task(event=None):

    text = task_entry.get().strip()

    if text == "":
        messagebox.showwarning(
            "Warning",
            "Please enter a task."
        )
        return

    # Check duplicate
    for task in tasks:

        if task["text"].lower() == text.lower():

            messagebox.showwarning(
                "Duplicate",
                "This task already exists."
            )
            return

    tasks.append({
        "text": text,
        "completed": False
    })

    save_tasks()
    refresh_tasks()

    task_entry.delete(0, tk.END)
    task_entry.focus()

    # Select newly added task
    new_index = len(tasks) - 1

    task_list.selection_clear(0, tk.END)
    task_list.selection_set(new_index)
    task_list.activate(new_index)
    task_list.see(new_index)


# =========================================================
# GET SELECTED TASK
# =========================================================

def get_selected_index():

    selected = task_list.curselection()

    if not selected:
        messagebox.showwarning(
            "No Task Selected",
            "Please click on a task first."
        )
        return None

    return selected[0]


# =========================================================
# SELECT TASK
# =========================================================

def select_task(event=None):

    selected = task_list.curselection()

    if not selected:
        return

    index = selected[0]

    # Put selected task into input box
    task_entry.delete(0, tk.END)
    task_entry.insert(0, tasks[index]["text"])

    # Make sure selection remains visible
    task_list.selection_clear(0, tk.END)
    task_list.selection_set(index)
    task_list.activate(index)


# =========================================================
# COMPLETE / UNCOMPLETE
# =========================================================

def toggle_complete():

    index = get_selected_index()

    if index is None:
        return

    tasks[index]["completed"] = not tasks[index]["completed"]

    save_tasks()
    refresh_tasks()

    # Keep selected
    task_list.selection_set(index)
    task_list.activate(index)
    task_list.see(index)


# =========================================================
# UPDATE TASK
# =========================================================

def update_task():

    index = get_selected_index()

    if index is None:
        return

    new_text = task_entry.get().strip()

    if new_text == "":
        messagebox.showwarning(
            "Warning",
            "Please enter the updated task."
        )
        return

    # Check duplicate
    for i, task in enumerate(tasks):

        if i != index and task["text"].lower() == new_text.lower():

            messagebox.showwarning(
                "Duplicate",
                "Another task with this name already exists."
            )
            return

    tasks[index]["text"] = new_text

    save_tasks()
    refresh_tasks()

    task_list.selection_set(index)
    task_list.activate(index)
    task_list.see(index)

    task_entry.delete(0, tk.END)


# =========================================================
# DELETE TASK
# =========================================================

def delete_task():

    index = get_selected_index()

    if index is None:
        return

    task_name = tasks[index]["text"]

    answer = messagebox.askyesno(
        "Delete Task",
        f"Delete this task?\n\n{task_name}"
    )

    if not answer:
        return

    tasks.pop(index)

    save_tasks()
    refresh_tasks()

    task_entry.delete(0, tk.END)


# =========================================================
# DELETE COMPLETED TASKS
# =========================================================

def delete_completed():

    completed = any(
        task["completed"] for task in tasks
    )

    if not completed:

        messagebox.showinfo(
            "Information",
            "There are no completed tasks."
        )
        return

    answer = messagebox.askyesno(
        "Delete Completed",
        "Delete all completed tasks?"
    )

    if not answer:
        return

    tasks[:] = [
        task for task in tasks
        if not task["completed"]
    ]

    save_tasks()
    refresh_tasks()

    task_entry.delete(0, tk.END)


# =========================================================
# CLEAR
# =========================================================

def clear_input():

    task_entry.delete(0, tk.END)

    task_list.selection_clear(0, tk.END)

    task_entry.focus()


# =========================================================
# COUNTER
# =========================================================

def update_counter():

    total = len(tasks)

    completed = sum(
        1 for task in tasks
        if task["completed"]
    )

    pending = total - completed

    counter_label.config(
        text=f"Total: {total}     Pending: {pending}     Completed: {completed}"
    )


# =========================================================
# MAIN WINDOW
# =========================================================

window = tk.Tk()

window.title("To-Do List")
window.geometry("700x700")

window.configure(
    bg="#1e1e1e"
)

window.resizable(
    False,
    False
)


# =========================================================
# TITLE
# =========================================================

title = tk.Label(
    window,
    text="TO-DO LIST",
    font=("Arial", 32, "bold"),
    bg="#1e1e1e",
    fg="white"
)

title.pack(pady=(30, 5))


subtitle = tk.Label(
    window,
    text="Manage your tasks easily",
    font=("Arial", 13),
    bg="#1e1e1e",
    fg="#aaaaaa"
)

subtitle.pack(pady=(0, 20))


# =========================================================
# ENTRY
# =========================================================

task_entry = tk.Entry(
    window,
    font=("Arial", 16),
    width=42,
    bg="white",
    fg="black",
    insertbackground="black"
)

task_entry.pack(pady=10)

task_entry.focus()


# =========================================================
# BUTTON FRAME
# =========================================================

button_frame = tk.Frame(
    window,
    bg="#1e1e1e"
)

button_frame.pack(pady=15)


button_style = {
    "font": ("Arial", 11, "bold"),
    "width": 14,
    "height": 1,
    "cursor": "hand2"
}


# =========================================================
# BUTTONS
# =========================================================

tk.Button(
    button_frame,
    text="Add Task",
    command=add_task,
    **button_style
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)


tk.Button(
    button_frame,
    text="Update",
    command=update_task,
    **button_style
).grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)


tk.Button(
    button_frame,
    text="Complete / Undo",
    command=toggle_complete,
    **button_style
).grid(
    row=0,
    column=2,
    padx=5,
    pady=5
)


tk.Button(
    button_frame,
    text="Delete",
    command=delete_task,
    **button_style
).grid(
    row=1,
    column=0,
    padx=5,
    pady=5
)


tk.Button(
    button_frame,
    text="Clear",
    command=clear_input,
    **button_style
).grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)


tk.Button(
    button_frame,
    text="Delete Completed",
    command=delete_completed,
    **button_style
).grid(
    row=1,
    column=2,
    padx=5,
    pady=5
)


# =========================================================
# COUNTER
# =========================================================

counter_label = tk.Label(
    window,
    text="Total: 0     Pending: 0     Completed: 0",
    font=("Arial", 12, "bold"),
    bg="#1e1e1e",
    fg="#cccccc"
)

counter_label.pack(pady=10)


# =========================================================
# LIST FRAME
# =========================================================

list_frame = tk.Frame(
    window,
    bg="#1e1e1e"
)

list_frame.pack(pady=10)


# =========================================================
# SCROLLBAR
# =========================================================

scrollbar = tk.Scrollbar(
    list_frame
)

scrollbar.pack(
    side=tk.RIGHT,
    fill=tk.Y
)


# =========================================================
# TASK LIST
# =========================================================

task_list = tk.Listbox(
    list_frame,

    width=52,
    height=13,

    font=("Arial", 14),

    bg="#292929",
    fg="white",

    selectbackground="#1976D2",
    selectforeground="white",

    # IMPORTANT FOR MAC
    selectmode=tk.SINGLE,
    exportselection=False,

    activestyle="none",

    yscrollcommand=scrollbar.set
)

task_list.pack(
    side=tk.LEFT
)


scrollbar.config(
    command=task_list.yview
)


# =========================================================
# MOUSE CLICK
# =========================================================

task_list.bind(
    "<ButtonRelease-1>",
    select_task
)


# =========================================================
# DOUBLE CLICK
# =========================================================

task_list.bind(
    "<Double-Button-1>",
    select_task
)


# =========================================================
# ENTER KEY
# =========================================================

task_entry.bind(
    "<Return>",
    add_task
)


# =========================================================
# LOAD DATA
# =========================================================

load_tasks()

refresh_tasks()


# =========================================================
# RUN APPLICATION
# =========================================================

window.mainloop()
