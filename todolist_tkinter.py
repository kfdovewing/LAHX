import tkinter as tk
from tkinter import messagebox

class TodoList:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("350x500")
        self.root.configure(bg="#eaf0f6")
        self.root.resizable(False,False)

        self.tasks = []
        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(
            self.root,
            text="To-Do",
            font=("Segoe UI", 24, "bold"),
            bg="#eaf0f6",
            fg="#2c3e50"
        )
        title.pack(pady=15)

        input_frame = tk.Frame(self.root, bg="#eaf0f6")
        input_frame.pack(pady=10)

        self.task_entry = tk.Entry(
            input_frame,
            font=("Segoe UI", 12),
            width=28,
            bd=0,
            highlightthickness=2,
            highlightbackground="#bdc3c7",
            highlightcolor="#3498db"
        )
        self.task_entry.pack(side="left", padx=(0, 10), ipady=6)

        add_btn = tk.Button(
            input_frame,
            text="+",
            font=("Segoe UI", 14, "bold"),
            bg="#3498db",
            bd=0,
            width=3,
            command=self.add_task
        )
        add_btn.pack(side="left")

        list_frame = tk.Frame(self.root, bg="#eaf0f6")
        list_frame.pack(pady=15, fill="both", expand=True)

        self.task_listbox = tk.Listbox(
            list_frame,
            font=("Segoe UI", 12),
            bg="white",
            fg="#2c3e50",
            selectbackground="#3498db",
            activestyle="none",
            bd=0,
            highlightthickness=0
        )
        self.task_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.task_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_listbox.yview)

        btn_frame = tk.Frame(self.root, bg="#eaf0f6")
        btn_frame.pack(pady=10)

        def style_button(btn, color):
            btn.config(
                font=("Segoe UI", 10, "bold"),
                bg=color,
                bd=0,
                padx=12,
                pady=6
            )

        done_btn = tk.Button(btn_frame, text="Done", command=self.mark_done)
        delete_btn = tk.Button(btn_frame, text="Delete", command=self.delete_task)
        clear_btn = tk.Button(btn_frame, text="Clear", command=self.clear_all)

        style_button(done_btn, "#2ecc71")
        style_button(delete_btn, "#e74c3c")
        style_button(clear_btn, "#7f8c8d")

        done_btn.pack(side="left", padx=5)
        delete_btn.pack(side="left", padx=5)
        clear_btn.pack(side="left", padx=5)

    def refresh_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for i, task in enumerate(self.tasks, start=1):
            prefix = "☑ " if task["done"] else "☐ "
            self.task_listbox.insert(tk.END, f"{prefix}{task['task']}")

    def add_task(self):
        text = self.task_entry.get().strip()
        if not text:
            return
        self.tasks.append({"task": text, "done": False})
        self.task_entry.delete(0, tk.END)
        self.refresh_listbox()

    def get_selected_index(self):
        sel = self.task_listbox.curselection()
        if not sel:
            messagebox.showinfo("Select Task", "Pick a task first.")
            return None
        return sel[0]

    def mark_done(self):
        i = self.get_selected_index()
        if i is None:
            return
        self.tasks[i]["done"] = True
        self.refresh_listbox()

    def delete_task(self):
        i = self.get_selected_index()
        if i is None:
            return
        if self.tasks[i]["done"] == True:
            self.tasks.pop(i)
            self.refresh_listbox()
        else:
            if messagebox.askyesno("Delete", "Delete this task? You won't get any coins."):
                self.tasks.pop(i)
                self.refresh_listbox()
    
    def clear_all(self):
        if messagebox.askyesno("Clear", "Delete all tasks? You won't get any coins."):
            self.tasks.clear()
            self.refresh_listbox()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoList(root)
    root.mainloop()
