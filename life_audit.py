import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import re
from datetime import datetime
from tinydb import TinyDB, Query

# Strict YYYY-MM-DD pattern
DATE_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}$')

class LifeAuditGUI:
    def __init__(self, master):
        self.master = master
        master.title("Life Audit Tracker")

        # Initialize TinyDB
        self.db_path = 'tasks.json'
        self.db = TinyDB(self.db_path)

        # Predefined domains
        self.domains = ['Health', 'Work', 'Finance', 'Personal']

        # Input frame
        input_frame = ttk.Frame(master)
        input_frame.pack(padx=10, pady=5, fill='x')

        ttk.Label(input_frame, text='Domain:').grid(row=0, column=0, sticky='w')
        self.domain_cb = ttk.Combobox(input_frame, values=self.domains)
        self.domain_cb.grid(row=0, column=1, sticky='ew')

        ttk.Label(input_frame, text='Responsibility:').grid(row=1, column=0, sticky='w')
        self.resp_entry = ttk.Entry(input_frame)
        self.resp_entry.grid(row=1, column=1, sticky='ew')

        ttk.Label(input_frame, text='Status:').grid(row=0, column=2, sticky='w')
        self.status_cb = ttk.Combobox(input_frame, values=['Not Started', 'In Progress', 'Done'])
        self.status_cb.grid(row=0, column=3, sticky='ew')

        ttk.Label(input_frame, text='Priority:').grid(row=1, column=2, sticky='w')
        self.prio_cb = ttk.Combobox(input_frame, values=['Low', 'Medium', 'High'])
        self.prio_cb.grid(row=1, column=3, sticky='ew')

        ttk.Label(input_frame, text='Actions:').grid(row=2, column=0, sticky='w')
        self.actions_entry = ttk.Entry(input_frame)
        self.actions_entry.grid(row=2, column=1, columnspan=3, sticky='ew')

        ttk.Label(input_frame, text='Notes:').grid(row=3, column=0, sticky='w')
        self.notes_entry = ttk.Entry(input_frame)
        self.notes_entry.grid(row=3, column=1, columnspan=3, sticky='ew')

        # Date frame
        date_frame = ttk.Frame(master)
        date_frame.pack(padx=10, pady=5, fill='x')

        ttk.Label(date_frame, text='Assigned Date:').grid(row=0, column=0, sticky='w')
        self.assigned_entry = ttk.Entry(date_frame)
        self.assigned_entry.grid(row=0, column=1, sticky='ew')
        self.assigned_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))

        ttk.Label(date_frame, text='Due Date:').grid(row=0, column=2, sticky='w')
        self.due_entry = ttk.Entry(date_frame)
        self.due_entry.grid(row=0, column=3, sticky='ew')

        ttk.Label(date_frame, text='Completed Date:').grid(row=1, column=0, sticky='w')
        self.completed_entry = ttk.Entry(date_frame)
        self.completed_entry.grid(row=1, column=1, sticky='ew')

        # Button frame
        btn_frame = ttk.Frame(master)
        btn_frame.pack(padx=10, pady=5)
        ttk.Button(btn_frame, text='Add Entry', command=self.add_entry).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='Delete Selected', command=self.delete_selected).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='Export CSV', command=self.save_csv).pack(side='left', padx=5)

        # Table frame
        table_frame = ttk.Frame(master)
        table_frame.pack(padx=10, pady=5, fill='both', expand=True)

        cols = ['domain','responsibility','status','priority','actions','notes','assigned_date','due_date','completed_date']
        self.tree = ttk.Treeview(table_frame, columns=cols, show='headings')
        for c in cols:
            self.tree.heading(c, text=c.replace('_',' ').title())
            self.tree.column(c, width=100, anchor='center')
        self.tree.pack(fill='both', expand=True)

        # File menu for loading/saving DBs
        menubar = tk.Menu(master)
        filemenu = tk.Menu(menubar, tearoff=False)
        filemenu.add_command(label="Load DB…", command=self.load_db)
        filemenu.add_command(label="New DB…", command=self.new_db)
        menubar.add_cascade(label="File", menu=filemenu)
        master.config(menu=menubar)

        # Load existing records
        self.load_entries()

    def load_entries(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for record in self.db.all():
            vals = [record.get(k, '') for k in ['domain','responsibility','status','priority','actions','notes','assigned_date','due_date','completed_date']]
            self.tree.insert('', 'end', iid=str(record.doc_id), values=vals)

    def validate_date(self, date_str):
        if not date_str:
            return True
        if not DATE_PATTERN.match(date_str):
            return False
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def add_entry(self):
        domain = self.domain_cb.get().strip()
        resp = self.resp_entry.get().strip()
        status = self.status_cb.get().strip()
        prio = self.prio_cb.get().strip()
        actions = self.actions_entry.get().strip()
        notes = self.notes_entry.get().strip()
        assigned = self.assigned_entry.get().strip()
        due = self.due_entry.get().strip()
        comp = self.completed_entry.get().strip()

        if not (domain and resp):
            messagebox.showerror('Error', 'Domain and Responsibility are required.')
            return
        for date_str in [assigned, due, comp]:
            if not self.validate_date(date_str):
                messagebox.showerror('Error', f'Invalid date: {date_str}')
                return

        entry = {
            'domain': domain,
            'responsibility': resp,
            'status': status,
            'priority': prio,
            'actions': actions,
            'notes': notes,
            'assigned_date': assigned,
            'due_date': due,
            'completed_date': comp
        }
        doc_id = self.db.insert(entry)
        self.tree.insert('', 'end', iid=str(doc_id), values=list(entry.values()))

        if domain not in self.domains:
            self.domains.append(domain)
            self.domain_cb['values'] = self.domains

        # Clear inputs
        for widget in [self.domain_cb, self.resp_entry, self.status_cb, self.prio_cb,
                       self.actions_entry, self.notes_entry,
                       self.assigned_entry, self.due_entry, self.completed_entry]:
            widget.delete(0, 'end')
        self.assigned_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))

    def delete_selected(self):
        for iid in self.tree.selection():
            self.db.remove(doc_ids=[int(iid)])
            self.tree.delete(iid)

    def save_csv(self):
        path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV Files','*.csv')])
        if not path:
            return
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Domain','Responsibility','Status','Priority','Actions','Notes','Assigned Date','Due Date','Completed Date'])
            for record in self.db.all():
                writer.writerow([record.get(k,'') for k in ['domain','responsibility','status','priority','actions','notes','assigned_date','due_date','completed_date']])
        messagebox.showinfo('Saved', f'Data exported to {path}')

    def load_db(self):
        path = filedialog.askopenfilename(title="Select Life-Audit DB", filetypes=[("JSON DB","*.json")])
        if not path:
            return
        try:
            self.db.close()
        except Exception:
            pass
        self.db_path = path
        self.db = TinyDB(self.db_path)
        self.load_entries()

    def new_db(self):
        path = filedialog.asksaveasfilename(title="Create New Life-Audit DB", defaultextension=".json", filetypes=[("JSON DB","*.json")])
        if not path:
            return
        try:
            self.db.close()
        except Exception:
            pass
        self.db_path = path
        self.db = TinyDB(self.db_path)
        self.load_entries()

if __name__ == '__main__':
    root = tk.Tk()
    LifeAuditGUI(root)
    root.mainloop()
