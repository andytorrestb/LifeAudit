import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import re
from datetime import date, datetime

class LifeAuditGUI:
    def __init__(self, root):
        self.root = root
        root.title("Weekly Life Audit")

        # Pre-defined domains
        self.domain_list = [
            "Finances",
            "Health",
            "Home & Environment",
            "Career & Education",
            "Relationships & Community",
            "Personal Growth & Hobbies",
            "Self‑Care & Well‑Being"
        ]

        # --- Main Input frame ---
        main_frame = ttk.Frame(root, padding=10)
        main_frame.pack(fill=tk.X)

        # Columns except dates
        main_labels = [
            "Domain",
            "Responsibility",
            "Status",
            "Priority",
            "Actions",
            "Notes"
        ]
        self.vars = {}

        for i, lbl in enumerate(main_labels):
            ttk.Label(main_frame, text=lbl).grid(row=0, column=i, padx=5, sticky=tk.W)
            if lbl == "Domain":
                cmb = ttk.Combobox(main_frame, width=20, values=self.domain_list, state="normal")
                cmb.set(self.domain_list[0])
                cmb.grid(row=1, column=i, padx=5)
                self.vars[lbl] = cmb
            elif lbl == "Status":
                cmb = ttk.Combobox(main_frame, width=12, state="readonly",
                                   values=["On Track", "Needs Attention", "Overdue"])
                cmb.current(0)
                cmb.grid(row=1, column=i, padx=5)
                self.vars[lbl] = cmb
            elif lbl == "Priority":
                cmb = ttk.Combobox(main_frame, width=12, state="readonly",
                                   values=["High", "Medium", "Low"])
                cmb.current(0)
                cmb.grid(row=1, column=i, padx=5)
                self.vars[lbl] = cmb
            else:
                ent = ttk.Entry(main_frame, width=20)
                ent.grid(row=1, column=i, padx=5)
                self.vars[lbl] = ent

        # --- Date Input frame ---
        date_frame = ttk.Frame(root, padding=(10,0,10,10))
        date_frame.pack(fill=tk.X)

        self.date_labels = ["Assigned Date", "Due Date", "Completed Date"]
        for j, lbl in enumerate(self.date_labels):
            ttk.Label(date_frame, text=lbl).grid(row=0, column=j, padx=5, sticky=tk.W)
            ent = ttk.Entry(date_frame, width=20)
            if lbl == "Assigned Date":
                ent.insert(0, date.today().strftime('%Y-%m-%d'))
            ent.grid(row=1, column=j, padx=5)
            self.vars[lbl] = ent

        # Buttons
        btn_frame = ttk.Frame(root, padding=(10,0,10,10))
        btn_frame.pack(fill=tk.X)
        ttk.Button(btn_frame, text="Add Entry", command=self.add_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Save to CSV", command=self.save_csv).pack(side=tk.RIGHT, padx=5)

        # --- Table frame ---
        all_labels = main_labels + self.date_labels
        self.tree = ttk.Treeview(root, columns=all_labels, show="headings", height=10)
        for c in all_labels:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120, anchor=tk.W)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0,10))

    def add_entry(self):
        vals = []
        for key, widget in self.vars.items():
            v = widget.get().strip()
            if not v:
                messagebox.showwarning("Missing Data", f"Please enter a value for '{key}'.")
                return
            # Enforce strict YYYY-MM-DD format
            if key in self.date_labels:
                if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', v):
                    messagebox.showerror("Invalid Date Format",
                        f"'{key}' must be in YYYY-MM-DD (zero-padded) format.")
                    return
                try:
                    datetime.strptime(v, '%Y-%m-%d')
                except ValueError:
                    messagebox.showerror("Invalid Date",
                        f"'{key}' is not a valid calendar date.")
                    return
            # Add new domain if necessary
            if key == "Domain" and v not in self.domain_list:
                self.domain_list.append(v)
                self.vars["Domain"]["values"] = self.domain_list
            vals.append(v)

        self.tree.insert("", tk.END, values=vals)

        # Reset inputs
        for key, widget in self.vars.items():
            if isinstance(widget, ttk.Entry):
                widget.delete(0, tk.END)
                if key == "Assigned Date":
                    widget.insert(0, date.today().strftime('%Y-%m-%d'))
            else:
                if key == "Domain":
                    widget.set(self.domain_list[0])
                else:
                    widget.current(0)

    def delete_selected(self):
        for item in self.tree.selection():
            self.tree.delete(item)

    def save_csv(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not path:
            return
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(self.tree["columns"])
            for row_id in self.tree.get_children():
                writer.writerow(self.tree.item(row_id)["values"])
        messagebox.showinfo("Saved", f"Table saved to:\n{path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LifeAuditGUI(root)
    root.mainloop()
