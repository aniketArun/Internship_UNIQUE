import tkinter as tk
from tkinter import ttk

# Function to update scrollbar when treeview is scrolled
def on_treeview_scroll(*args):
    tree.yview(*args)

# Create the main window
root = tk.Tk()
root.title("Treeview with Scrollbar")

# Create the Treeview with embedded scrollbar
tree = ttk.Treeview(root, columns=("Name", "Age"), show="headings", height=10)

tree.heading("Name", text="Name")
tree.heading("Age", text="Age")

# Insert some dummy data for demonstration
for i in range(1, 101):
    tree.insert("", i, values=(f"Name {i}", f"{20 + i}"))

# Create the embedded scrollbar for the Treeview
vsb = ttk.Scrollbar(root, orient="vertical", command=on_treeview_scroll)
tree.configure(yscrollcommand=vsb.set)

# Place the Treeview and the embedded scrollbar in the window
tree.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.W, tk.E))
vsb.grid(column=1, row=0, sticky=(tk.N, tk.S))

# Make the columns resizable
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.mainloop()
