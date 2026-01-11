"""
Staff Management for Zoo Management System (Admin Only)
Save as: staff_management_integrated.py
"""

from common import *
from tkinter import scrolledtext

class StaffManagement:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("Staff Management")
        self.root.geometry("1200x700")
        self.root.configure(bg="#ecf0f1")
        
        # Top Bar
        top_frame = create_top_bar(self.root, "Staff Management (Admin Only)", user)
        tk.Button(top_frame, text="Close", bg="#95a5a6", fg="white",
                 command=self.root.destroy).pack(side="right", padx=10)
        
        # Main Frame
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Buttons
        btn_frame = create_button_frame(main_frame)
        
        create_button(btn_frame, "➕ Add Staff", self.add_staff, "#27ae60").pack(side="left", padx=5)
        create_button(btn_frame, "✏️ Edit Staff", self.edit_staff, "#3498db").pack(side="left", padx=5)
        create_button(btn_frame, "🗑️ Delete Staff", self.delete_staff, "#e74c3c").pack(side="left", padx=5)
        create_button(btn_frame, "📋 Assign Task", self.assign_task, "#9b59b6").pack(side="left", padx=5)
        create_button(btn_frame, "🔄 Refresh", self.load_staff, "#95a5a6").pack(side="left", padx=5)
        
        # Search
        search_frame = tk.Frame(main_frame, bg="#ecf0f1")
        search_frame.pack(fill="x", pady=10)
        
        tk.Label(search_frame, text="Search:", font=("Arial", 11), bg="#ecf0f1").pack(side="left", padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Arial", 11), width=30)
        self.search_entry.pack(side="left", padx=5)
        
        # Treeview
        columns = ("ID", "Username", "Full Name", "Role", "Email", "Phone", "Status")
        widths = [50, 120, 150, 100, 180, 120, 100]
        self.tree = create_treeview(main_frame, columns, widths)
        
        # Load data
        self.load_staff()
    
    def load_staff(self):
        """Load all staff members"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if db.connect():
            users = db.get_all_users()
            db.disconnect()
            
            for user in users:
                self.tree.insert("", "end", values=(
                    user['user_id'],
                    user['username'],
                    user['full_name'],
                    user['role'],
                    user['email'],
                    user['phone'],
                    user['status']
                ))
    
    def add_staff(self):
        """Add new staff member"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Staff Member")
        dialog.geometry("450x650")
        dialog.configure(bg="#ecf0f1")
        
        tk.Label(dialog, text="Add New Staff Member", font=("Arial", 16, "bold"), bg="#ecf0f1").pack(pady=10)
        
        fields_frame = tk.Frame(dialog, bg="#ecf0f1")
        fields_frame.pack(pady=10, padx=20)
        
        tk.Label(fields_frame, text="Username:", font=("Arial", 11), bg="#ecf0f1").grid(row=0, column=0, sticky="w", pady=5)
        username_entry = tk.Entry(fields_frame, font=("Arial", 11), width=30)
        username_entry.grid(row=0, column=1, pady=5)
        
        tk.Label(fields_frame, text="Password:", font=("Arial", 11), bg="#ecf0f1").grid(row=1, column=0, sticky="w", pady=5)
        password_entry = tk.Entry(fields_frame, font=("Arial", 11), width=30, show="●")
        password_entry.grid(row=1, column=1, pady=5)
        
        tk.Label(fields_frame, text="Full Name:", font=("Arial", 11), bg="#ecf0f1").grid(row=2, column=0, sticky="w", pady=5)
        name_entry = tk.Entry(fields_frame, font=("Arial", 11), width=30)
        name_entry.grid(row=2, column=1, pady=5)
        
        tk.Label(fields_frame, text="Role:", font=("Arial", 11), bg="#ecf0f1").grid(row=3, column=0, sticky="w", pady=5)
        role_combo = ttk.Combobox(fields_frame, values=["Admin", "Staff", "Senior Staff"], 
                                  font=("Arial", 11), width=28)
        role_combo.current(1)
        role_combo.grid(row=3, column=1, pady=5)
        
        tk.Label(fields_frame, text="Email:", font=("Arial", 11), bg="#ecf0f1").grid(row=4, column=0, sticky="w", pady=5)
        email_entry = tk.Entry(fields_frame, font=("Arial", 11), width=30)
        email_entry.grid(row=4, column=1, pady=5)
        
        tk.Label(fields_frame, text="Phone:", font=("Arial", 11), bg="#ecf0f1").grid(row=5, column=0, sticky="w", pady=5)
        phone_entry = tk.Entry(fields_frame, font=("Arial", 11), width=30)
        phone_entry.grid(row=5, column=1, pady=5)
        
        tk.Label(fields_frame, text="Join Date:", font=("Arial", 11), bg="#ecf0f1").grid(row=6, column=0, sticky="w", pady=5)
        date_entry = tk.Entry(fields_frame, font=("Arial", 11), width=30)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_entry.grid(row=6, column=1, pady=5)
        
        tk.Label(fields_frame, text="Status:", font=("Arial", 11), bg="#ecf0f1").grid(row=7, column=0, sticky="w", pady=5)
        status_combo = ttk.Combobox(fields_frame, values=["Active", "On Leave", "Inactive"], 
                                    font=("Arial", 11), width=28)
        status_combo.current(0)
        status_combo.grid(row=7, column=1, pady=5)
        
        def save():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            full_name = name_entry.get().strip()
            role = role_combo.get()
            email = email_entry.get().strip()
            phone = phone_entry.get().strip()
            join_date = date_entry.get().strip()
            status = status_combo.get()
            
            if not all([username, password, full_name, role, email]):
                show_warning("Warning", "Please fill all required fields")
                return
            
            if not validate_email(email):
                show_error("Error", "Invalid email format")
                return
            
            if not validate_date(join_date):
                show_error("Error", "Invalid date format")
                return
            
            if db.connect():
                if db.add_user(username, password, full_name, role, email, phone, join_date, status):
                    db.disconnect()
                    show_success("Success", "Staff member added successfully!")
                    dialog.destroy()
                    self.load_staff()
                else:
                    db.disconnect()
        
        tk.Button(dialog, text="Save", bg="#27ae60", fg="white", 
                 font=("Arial", 12, "bold"), width=15, command=save).pack(pady=20)
    
    def edit_staff(self):
        """Edit selected staff member"""
        values = get_selected_item(self.tree)
        if not values:
            return
        
        user_id = values[0]
        
        if user_id == self.user['user_id']:
            show_warning("Warning", "You cannot edit your own account here")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Staff Member")
        dialog.geometry("450x550")
        dialog.configure(bg="#ecf0f1")
        
        tk.Label(dialog, text="Edit Staff Member", font=("Arial", 16, "bold"), bg="#ecf0f1").pack(pady=10)
        
        fields_frame = tk.Frame(dialog, bg="#ecf0f1")
        fields_frame.pack(pady=10, padx=20)
        
        tk.Label(fields_frame, text="Full Name:", font=("Arial", 11), bg="#ecf0f1").grid(row=0, column=0, sticky="w", pady=5)
        name_entry = tk.Entry(fields_frame, font=("Arial", 11), width=30)
        name_entry.insert(0, values[2])
        name_entry.grid(row=0, column=1, pady=5)
        
        tk.Label(fields_frame, text="Role:", font=("Arial", 11), bg="#ecf0f1").grid(row=1, column=0, sticky="w", pady=5)
        role_combo = ttk.Combobox(fields_frame, values=["Admin", "Staff", "Senior Staff"], 
                                  font=("Arial", 11), width=28)
        role_combo.set(values[3])
        role_combo.grid(row=1, column=1, pady=5)
        
        tk.Label(fields_frame, text="Email:", font=("Arial", 11), bg="#ecf0f1").grid(row=2, column=0, sticky="w", pady=5)
        email_entry = tk.Entry(fields_frame, font=("Arial", 11), width=30)
        email_entry.insert(0, values[4])
        email_entry.grid(row=2, column=1, pady=5)
        
        tk.Label(fields_frame, text="Phone:", font=("Arial", 11), bg="#ecf0f1").grid(row=3, column=0, sticky="w", pady=5)
        phone_entry = tk.Entry(fields_frame, font=("Arial", 11), width=30)
        phone_entry.insert(0, values[5])
        phone_entry.grid(row=3, column=1, pady=5)
        
        tk.Label(fields_frame, text="Status:", font=("Arial", 11), bg="#ecf0f1").grid(row=4, column=0, sticky="w", pady=5)
        status_combo = ttk.Combobox(fields_frame, values=["Active", "On Leave", "Inactive"], 
                                    font=("Arial", 11), width=28)
        status_combo.set(values[6])
        status_combo.grid(row=4, column=1, pady=5)
        
        def update():
            if db.connect():
                if db.update_user(user_id, name_entry.get(), role_combo.get(), 
                                 email_entry.get(), phone_entry.get(), status_combo.get()):
                    db.disconnect()
                    show_success("Success", "Staff member updated successfully!")
                    dialog.destroy()
                    self.load_staff()
                else:
                    db.disconnect()
        
        tk.Button(dialog, text="Update", bg="#3498db", fg="white", 
                 font=("Arial", 12, "bold"), width=15, command=update).pack(pady=20)
    
    def delete_staff(self):
        """Delete selected staff member"""
        values = get_selected_item(self.tree)
        if not values:
            return
        
        user_id = values[0]
        
        if user_id == self.user['user_id']:
            show_error("Error", "You cannot delete your own account")
            return
        
        if confirm_action("Confirm", f"Delete staff member '{values[2]}'?\nThis action cannot be undone."):
            if db.connect():
                if db.delete_user(user_id):
                    db.disconnect()
                    show_success("Success", "Staff member deleted successfully!")
                    self.load_staff()
                else:
                    db.disconnect()
    
    def assign_task(self):
        """Assign task to selected staff member"""
        values = get_selected_item(self.tree)
        if not values:
            return
        
        user_id = values[0]
        staff_name = values[2]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Assign Task")
        dialog.geometry("500x450")
        dialog.configure(bg="#ecf0f1")
        
        tk.Label(dialog, text=f"Assign Task to {staff_name}", 
                font=("Arial", 16, "bold"), bg="#ecf0f1").pack(pady=10)
        
        fields_frame = tk.Frame(dialog, bg="#ecf0f1")
        fields_frame.pack(pady=10, padx=20)
        
        tk.Label(fields_frame, text="Task Description:", font=("Arial", 11), bg="#ecf0f1").pack(pady=5)
        task_text = scrolledtext.ScrolledText(fields_frame, font=("Arial", 11), width=45, height=8)
        task_text.pack(pady=5)
        
        tk.Label(fields_frame, text="Due Date (YYYY-MM-DD):", font=("Arial", 11), bg="#ecf0f1").pack(pady=5)
        date_entry = tk.Entry(fields_frame, font=("Arial", 11), width=35)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_entry.pack(pady=5)
        
        tk.Label(fields_frame, text="Priority:", font=("Arial", 11), bg="#ecf0f1").pack(pady=5)
        priority_combo = ttk.Combobox(fields_frame, values=["Low", "Medium", "High", "Urgent"], 
                                     font=("Arial", 11), width=33)
        priority_combo.current(1)
        priority_combo.pack(pady=5)
        
        def assign():
            task_description = task_text.get("1.0", "end-1c").strip()
            due_date = date_entry.get().strip()
            priority = priority_combo.get()
            
            if not task_description:
                show_warning("Warning", "Please enter a task description")
                return
            
            if not validate_date(due_date):
                show_error("Error", "Invalid date format")
                return
            
            if db.connect():
                if db.add_task(user_id, task_description, due_date, priority, self.user['user_id']):
                    db.disconnect()
                    show_success("Success", f"Task assigned to {staff_name}!")
                    dialog.destroy()
                else:
                    db.disconnect()
        
        tk.Button(dialog, text="Assign Task", bg="#9b59b6", fg="white", 
                 font=("Arial", 12, "bold"), width=15, command=assign).pack(pady=20)


if __name__ == "__main__":
    test_user = {'user_id': 1, 'full_name': 'Admin', 'role': 'Admin'}
    root = tk.Tk()
    StaffManagement(root, test_user)
    root.mainloop()
