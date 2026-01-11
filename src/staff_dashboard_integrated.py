"""
Staff Dashboard for Zoo Management System
Save as: staff_dashboard_integrated.py
"""

from common import *

class StaffDashboard:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("Zoo Management System - Staff Dashboard")
        self.root.geometry("1200x700")
        self.root.configure(bg="#ecf0f1")
        
        # Top Bar
        top_frame = create_top_bar(self.root, "Staff Dashboard", user, bg_color="#16a085")
        
        tk.Button(top_frame, text="Logout", 
                 bg="#e74c3c", fg="white",
                 font=("Arial", 11),
                 command=lambda: NavigationManager.logout(self.root)).pack(side="right", padx=10)
        
        # Main Container
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(fill="both", expand=True)
        
        # Left Menu
        self.create_menu(main_frame)
        
        # Content Area - Tasks
        content_frame = tk.Frame(main_frame, bg="#ecf0f1")
        content_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(content_frame, text="My Daily Tasks", 
                font=("Arial", 18, "bold"),
                bg="#ecf0f1").pack(pady=10)
        
        # Load and display tasks
        self.create_tasks(content_frame)
    
    def create_menu(self, parent):
        """Create left navigation menu"""
        menu_frame = tk.Frame(parent, bg="#1abc9c", width=250)
        menu_frame.pack(side="left", fill="y")
        
        tk.Label(menu_frame, text="Navigation", 
                font=("Arial", 14, "bold"),
                bg="#1abc9c", fg="white").pack(pady=20)
        
        menu_items = [
            ("📋 My Tasks", lambda: None),
            ("🦁 Animal Records", lambda: NavigationManager.open_animal_records(self.user, self.root)),
            ("🍖 Feeding Schedule", lambda: NavigationManager.open_feeding_schedule(self.user, self.root)),
            ("💊 Health Updates", lambda: NavigationManager.open_health_updates(self.user, self.root))
        ]
        
        for text, command in menu_items:
            tk.Button(menu_frame, text=text, 
                     font=("Arial", 12), 
                     bg="#16a085", fg="white",
                     width=25, height=2, 
                     relief="flat",
                     anchor="w",
                     command=command).pack(pady=2, padx=5)
    
    def create_tasks(self, parent):
        """Create tasks display"""
        task_frame = tk.LabelFrame(parent, text="Today's Tasks", 
                                   font=("Arial", 14, "bold"), 
                                   bg="#ecf0f1")
        task_frame.pack(fill="both", expand=True, pady=10)
        
        # Get tasks from database
        if db.connect():
            tasks = db.get_user_tasks(self.user['user_id'])
            db.disconnect()
        else:
            tasks = []
        
        if tasks:
            for task in tasks:
                self.create_task_item(task_frame, task)
        else:
            tk.Label(task_frame, text="No tasks assigned", 
                    font=("Arial", 14),
                    bg="#ecf0f1", fg="#7f8c8d").pack(pady=50)
    
    def create_task_item(self, parent, task):
        """Create individual task item"""
        task_item = tk.Frame(parent, bg="white", relief="solid", borderwidth=1)
        task_item.pack(fill="x", padx=10, pady=5)
        
        # Task info frame
        info_frame = tk.Frame(task_item, bg="white")
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Task description
        tk.Label(info_frame, text=f"• {task['task_description']}", 
                font=("Arial", 11, "bold"), 
                bg="white", anchor="w").pack(anchor="w")
        
        # Due date and priority
        details = f"Due: {format_date(task['due_date'])} | Priority: {task['priority']}"
        tk.Label(info_frame, text=details, 
                font=("Arial", 9), 
                bg="white", fg="#7f8c8d", anchor="w").pack(anchor="w")
        
        # Status
        status_color = "#27ae60" if task['status'] == "Completed" else "#f39c12"
        tk.Label(task_item, text=task['status'], 
                font=("Arial", 10, "bold"), 
                bg="white", fg=status_color).pack(side="right", padx=10)
        
        # Complete button (only for pending tasks)
        if task['status'] == "Pending":
            tk.Button(task_item, text="Mark Complete", 
                     bg="#3498db", fg="white",
                     command=lambda: self.complete_task(task['task_id'])).pack(side="right", padx=5)
    
    def complete_task(self, task_id):
        """Mark task as completed"""
        if confirm_action("Confirm", "Mark this task as completed?"):
            if db.connect():
                if db.update_task_status(task_id, "Completed"):
                    db.disconnect()
                    show_success("Success", "Task marked as completed!")
                    # Refresh dashboard
                    self.root.destroy()
                    NavigationManager.open_staff_dashboard(self.user)
                else:
                    db.disconnect()
                    show_error("Error", "Failed to update task")


if __name__ == "__main__":
    # Test user
    test_user = {
        'user_id': 2,
        'username': 'staff1',
        'full_name': 'Staff Member',
        'role': 'Staff'
    }
    root = tk.Tk()
    StaffDashboard(root, test_user)
    root.mainloop()
