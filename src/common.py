"""
Common Module for Zoo Management System
Save as: common.py
Import this file in all UI files: from common import *
"""

import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import hashlib

# ==================== DATABASE CONNECTION CLASS ====================

class DatabaseConnection:
    """Handles all database operations"""
    
    def __init__(self):
        self.host = 'localhost'
        self.database = 'zoo_management'
        self.user = 'root'  # ← CHANGE THIS to your MySQL username
        self.password = 'pochacco2007#'  # ← CHANGE THIS to your MySQL password
        self.connection = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return self.connection.is_connected()
        except Error as e:
            print(f"Database Error: {e}")
            messagebox.showerror("Database Error", f"Could not connect to database:\n{e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query, params=None, fetch=False):
        """Execute a query with error handling"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                cursor.close()
                return result
            else:
                self.connection.commit()
                cursor.close()
                return True
        except Error as e:
            print(f"Query Error: {e}")
            messagebox.showerror("Query Error", f"Database operation failed:\n{e}")
            return [] if fetch else False
    
    # ========== USER/AUTHENTICATION ==========
    
    def validate_login(self, username, password):
        """Validate user login"""
        query = "SELECT * FROM users WHERE username = %s AND password = %s AND status = 'Active'"
        result = self.execute_query(query, (username, password), fetch=True)
        return result[0] if result else None
    
    def get_all_users(self):
        """Get all users"""
        query = "SELECT * FROM users ORDER BY user_id"
        return self.execute_query(query, fetch=True)
    
    def add_user(self, username, password, full_name, role, email, phone, join_date, status):
        """Add new user"""
        query = """
            INSERT INTO users (username, password, full_name, role, email, phone, join_date, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        return self.execute_query(query, (username, password, full_name, role, email, phone, join_date, status))
    
    def update_user(self, user_id, full_name, role, email, phone, status):
        """Update user"""
        query = """
            UPDATE users SET full_name=%s, role=%s, email=%s, phone=%s, status=%s
            WHERE user_id=%s
        """
        return self.execute_query(query, (full_name, role, email, phone, status, user_id))
    
    def delete_user(self, user_id):
        """Delete user"""
        query = "DELETE FROM users WHERE user_id = %s"
        return self.execute_query(query, (user_id,))
    
    # ========== ANIMALS ==========
    
    def get_all_animals(self):
        """Get all animals"""
        query = "SELECT * FROM animals ORDER BY animal_id"
        return self.execute_query(query, fetch=True)
    
    def add_animal(self, name, species, age, gender, enclosure_id, health_status, arrival_date):
        """Add new animal"""
        query = """
            INSERT INTO animals (name, species, age, gender, enclosure_id, health_status, arrival_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        return self.execute_query(query, (name, species, age, gender, enclosure_id, health_status, arrival_date))
    
    def update_animal(self, animal_id, name, species, age, gender, enclosure_id, health_status):
        """Update animal"""
        query = """
            UPDATE animals SET name=%s, species=%s, age=%s, gender=%s, enclosure_id=%s, health_status=%s
            WHERE animal_id=%s
        """
        return self.execute_query(query, (name, species, age, gender, enclosure_id, health_status, animal_id))
    
    def delete_animal(self, animal_id):
        """Delete animal"""
        query = "DELETE FROM animals WHERE animal_id = %s"
        return self.execute_query(query, (animal_id,))
    
    def search_animals(self, search_term):
        """Search animals"""
        query = "SELECT * FROM animals WHERE name LIKE %s OR species LIKE %s"
        pattern = f"%{search_term}%"
        return self.execute_query(query, (pattern, pattern), fetch=True)
    
    # ========== ENCLOSURES ==========
    
    def get_all_enclosures(self):
        """Get all enclosures"""
        query = "SELECT * FROM enclosures ORDER BY enclosure_id"
        return self.execute_query(query, fetch=True)
    
    def add_enclosure(self, enclosure_id, name, enc_type, capacity, current_occupancy, condition_status):
        """Add new enclosure"""
        query = """
            INSERT INTO enclosures (enclosure_id, name, type, capacity, current_occupancy, condition_status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        return self.execute_query(query, (enclosure_id, name, enc_type, capacity, current_occupancy, condition_status))
    
    def update_enclosure(self, enclosure_id, name, enc_type, capacity, current_occupancy, condition_status):
        """Update enclosure"""
        query = """
            UPDATE enclosures SET name=%s, type=%s, capacity=%s, current_occupancy=%s, condition_status=%s
            WHERE enclosure_id=%s
        """
        return self.execute_query(query, (name, enc_type, capacity, current_occupancy, condition_status, enclosure_id))
    
    def delete_enclosure(self, enclosure_id):
        """Delete enclosure"""
        query = "DELETE FROM enclosures WHERE enclosure_id = %s"
        return self.execute_query(query, (enclosure_id,))
    
    # ========== FEEDING SCHEDULE ==========
    
    def get_all_feeding_schedules(self):
        """Get all feeding schedules"""
        query = """
            SELECT fs.schedule_id, CONCAT(a.name, ' (', a.species, ')') as animal_name, 
                   fs.feed_time, fs.food_type, fs.quantity, u.full_name as staff_name,
                   fs.schedule_date, fs.status, a.animal_id, u.user_id as staff_id
            FROM feeding_schedule fs
            JOIN animals a ON fs.animal_id = a.animal_id
            JOIN users u ON fs.staff_id = u.user_id
            ORDER BY fs.schedule_date DESC, fs.feed_time
        """
        return self.execute_query(query, fetch=True)
    
    def add_feeding_schedule(self, animal_id, feed_time, food_type, quantity, staff_id, schedule_date):
        """Add feeding schedule"""
        query = """
            INSERT INTO feeding_schedule (animal_id, feed_time, food_type, quantity, staff_id, schedule_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        return self.execute_query(query, (animal_id, feed_time, food_type, quantity, staff_id, schedule_date))
    
    def delete_feeding_schedule(self, schedule_id):
        """Delete feeding schedule"""
        query = "DELETE FROM feeding_schedule WHERE schedule_id = %s"
        return self.execute_query(query, (schedule_id,))
    
    def update_feeding_status(self, schedule_id, status):
        """Update feeding status"""
        query = "UPDATE feeding_schedule SET status = %s WHERE schedule_id = %s"
        return self.execute_query(query, (status, schedule_id))
    
    # ========== HEALTH RECORDS ==========
    
    def get_all_health_records(self):
        """Get all health records"""
        query = """
            SELECT hr.record_id, CONCAT(a.name, ' (', a.species, ')') as animal_name,
                   hr.check_date, hr.condition_desc, hr.treatment, hr.vet_name, hr.next_checkup,
                   a.animal_id
            FROM health_records hr
            JOIN animals a ON hr.animal_id = a.animal_id
            ORDER BY hr.check_date DESC
        """
        return self.execute_query(query, fetch=True)
    
    def add_health_record(self, animal_id, check_date, condition_desc, treatment, vet_notes, vet_name, next_checkup):
        """Add health record"""
        query = """
            INSERT INTO health_records (animal_id, check_date, condition_desc, treatment, vet_notes, vet_name, next_checkup)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        return self.execute_query(query, (animal_id, check_date, condition_desc, treatment, vet_notes, vet_name, next_checkup))
    
    def delete_health_record(self, record_id):
        """Delete health record"""
        query = "DELETE FROM health_records WHERE record_id = %s"
        return self.execute_query(query, (record_id,))
    
    # ========== TASKS ==========
    
    def get_user_tasks(self, user_id):
        """Get tasks for specific user"""
        query = """
            SELECT task_id, task_description, due_date, priority, status
            FROM tasks WHERE staff_id = %s
            ORDER BY due_date, priority DESC
        """
        return self.execute_query(query, (user_id,), fetch=True)
    
    def add_task(self, staff_id, task_description, due_date, priority, assigned_by):
        """Add new task"""
        query = """
            INSERT INTO tasks (staff_id, task_description, due_date, priority, assigned_by)
            VALUES (%s, %s, %s, %s, %s)
        """
        return self.execute_query(query, (staff_id, task_description, due_date, priority, assigned_by))
    
    def update_task_status(self, task_id, status):
        """Update task status"""
        query = "UPDATE tasks SET status = %s WHERE task_id = %s"
        return self.execute_query(query, (status, task_id))
    
    # ========== STATISTICS ==========
    
    def get_dashboard_stats(self):
        """Get dashboard statistics"""
        stats = {}
        
        # Total animals
        result = self.execute_query("SELECT COUNT(*) as count FROM animals", fetch=True)
        stats['total_animals'] = result[0]['count'] if result else 0
        
        # Total staff
        result = self.execute_query("SELECT COUNT(*) as count FROM users WHERE status='Active'", fetch=True)
        stats['total_staff'] = result[0]['count'] if result else 0
        
        # Total enclosures
        result = self.execute_query("SELECT COUNT(*) as count FROM enclosures", fetch=True)
        stats['total_enclosures'] = result[0]['count'] if result else 0
        
        return stats


# ==================== GLOBAL DATABASE INSTANCE ====================

# Create a single database instance that all modules can use
db = DatabaseConnection()


# ==================== NAVIGATION MANAGER ====================

class NavigationManager:
    """Manages navigation between windows"""
    
    current_window = None
    current_user = None
    
    @staticmethod
    def open_login(root=None):
        """Open login window"""
        if root:
            root.destroy()
        
        from login_integrated import LoginPage
        new_root = tk.Tk()
        LoginPage(new_root)
        new_root.mainloop()
    
    @staticmethod
    def open_admin_dashboard(user, current_window=None):
        """Open admin dashboard"""
        if current_window:
            current_window.destroy()
        
        from admin_dashboard_integrated import AdminDashboard
        new_root = tk.Tk()
        NavigationManager.current_user = user
        AdminDashboard(new_root, user)
        new_root.mainloop()
    
    @staticmethod
    def open_staff_dashboard(user, current_window=None):
        """Open staff dashboard"""
        if current_window:
            current_window.destroy()
        
        from staff_dashboard_integrated import StaffDashboard
        new_root = tk.Tk()
        NavigationManager.current_user = user
        StaffDashboard(new_root, user)
        new_root.mainloop()
    
    @staticmethod
    def open_animal_records(user, current_window=None):
        """Open animal records window"""
        from animal_records_integrated import AnimalRecords
        new_window = tk.Toplevel(current_window) if current_window else tk.Tk()
        AnimalRecords(new_window, user)
    
    @staticmethod
    def open_feeding_schedule(user, current_window=None):
        """Open feeding schedule window"""
        from feeding_schedule_integrated import FeedingSchedule
        new_window = tk.Toplevel(current_window) if current_window else tk.Tk()
        FeedingSchedule(new_window, user)
    
    @staticmethod
    def open_health_updates(user, current_window=None):
        """Open health updates window"""
        from health_updates_integrated import HealthUpdates
        new_window = tk.Toplevel(current_window) if current_window else tk.Tk()
        HealthUpdates(new_window, user)
    
    @staticmethod
    def open_enclosure_management(user, current_window=None):
        """Open enclosure management window"""
        from enclosure_management_integrated import EnclosureManagement
        new_window = tk.Toplevel(current_window) if current_window else tk.Tk()
        EnclosureManagement(new_window, user)
    
    @staticmethod
    def open_staff_management(user, current_window=None):
        """Open staff management window (Admin only)"""
        if user['role'] != 'Admin':
            messagebox.showwarning("Access Denied", "Only administrators can access staff management")
            return
        
        from staff_management_integrated import StaffManagement
        new_window = tk.Toplevel(current_window) if current_window else tk.Tk()
        StaffManagement(new_window, user)
    
    @staticmethod
    def logout(current_window):
        """Logout and return to login screen"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            NavigationManager.current_user = None
            NavigationManager.open_login(current_window)


# ==================== UTILITY FUNCTIONS ====================

def format_date(date_obj):
    """Format date object to string"""
    if isinstance(date_obj, str):
        return date_obj
    return date_obj.strftime("%Y-%m-%d") if date_obj else ""

def format_time(time_obj):
    """Format time object to string"""
    if isinstance(time_obj, str):
        return time_obj
    return str(time_obj) if time_obj else ""

def validate_date(date_string):
    """Validate date string format YYYY-MM-DD"""
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_email(email):
    """Basic email validation"""
    return "@" in email and "." in email.split("@")[1]

def show_error(title, message):
    """Show error message"""
    messagebox.showerror(title, message)

def show_success(title, message):
    """Show success message"""
    messagebox.showinfo(title, message)

def show_warning(title, message):
    """Show warning message"""
    messagebox.showwarning(title, message)

def confirm_action(title, message):
    """Show confirmation dialog"""
    return messagebox.askyesno(title, message)


# ==================== COMMON UI COMPONENTS ====================

def create_top_bar(parent, title, user, bg_color="#34495e"):
    """Create common top bar for all windows"""
    top_frame = tk.Frame(parent, bg=bg_color, height=80)
    top_frame.pack(fill="x")
    
    tk.Label(top_frame, text=title, 
            font=("Arial", 20, "bold"), 
            bg=bg_color, fg="white").pack(side="left", padx=20, pady=20)
    
    if user:
        tk.Label(top_frame, text=f"Welcome, {user['full_name']} ({user['role']})", 
                font=("Arial", 12), 
                bg=bg_color, fg="white").pack(side="right", padx=20)
    
    return top_frame

def create_button_frame(parent):
    """Create common button frame"""
    btn_frame = tk.Frame(parent, bg="#ecf0f1")
    btn_frame.pack(fill="x", pady=10)
    return btn_frame

def create_treeview(parent, columns, widths=None):
    """Create common treeview with scrollbar"""
    tree_frame = tk.Frame(parent)
    tree_frame.pack(fill="both", expand=True)
    
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
    
    # Set column headings and widths
    for i, col in enumerate(columns):
        tree.heading(col, text=col)
        width = widths[i] if widths and i < len(widths) else 100
        tree.column(col, width=width)
    
    # Scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    return tree

def create_button(parent, text, command, bg_color, width=15):
    """Create styled button"""
    return tk.Button(parent, text=text, 
                    bg=bg_color, fg="white", 
                    font=("Arial", 11, "bold"),
                    width=width,
                    command=command)

def get_selected_item(tree):
    """Get selected item from treeview"""
    selected = tree.selection()
    if not selected:
        show_warning("Warning", "Please select an item first")
        return None
    return tree.item(selected[0])['values']


# ==================== DATA HELPERS ====================

def get_animal_names():
    """Get list of all animal names for dropdowns"""
    if db.connect():
        animals = db.get_all_animals()
        db.disconnect()
        return [f"{a['name']} ({a['species']})" for a in animals]
    return []

def get_staff_names():
    """Get list of all staff names for dropdowns"""
    if db.connect():
        staff = db.get_all_users()
        db.disconnect()
        return [s['full_name'] for s in staff if s['status'] == 'Active']
    return []

def get_enclosure_ids():
    """Get list of all enclosure IDs for dropdowns"""
    if db.connect():
        enclosures = db.get_all_enclosures()
        db.disconnect()
        return [e['enclosure_id'] for e in enclosures]
    return []

def get_animal_id_by_name(name_with_species):
    """Extract animal ID from 'Name (Species)' format"""
    if db.connect():
        animals = db.get_all_animals()
        db.disconnect()
        for animal in animals:
            if f"{animal['name']} ({animal['species']})" == name_with_species:
                return animal['animal_id']
    return None

def get_user_id_by_name(full_name):
    """Get user ID by full name"""
    if db.connect():
        users = db.get_all_users()
        db.disconnect()
        for user in users:
            if user['full_name'] == full_name:
                return user['user_id']
    return None


# ==================== CONFIGURATION ====================

# Color scheme
COLORS = {
    'primary': '#34495e',
    'secondary': '#2c3e50',
    'success': '#27ae60',
    'danger': '#e74c3c',
    'warning': '#f39c12',
    'info': '#3498db',
    'light': '#ecf0f1',
    'dark': '#2c3e50'
}

# Application info
APP_NAME = "Zoo Management System"
APP_VERSION = "1.0.0"

print(f"{APP_NAME} v{APP_VERSION} - Common module loaded successfully!")
