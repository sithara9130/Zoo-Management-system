"""
Feeding Schedule for Zoo Management System
Save as: feeding_schedule_integrated.py
"""

from common import *

class FeedingSchedule:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("Feeding Schedule")
        self.root.geometry("1200x700")
        self.root.configure(bg="#ecf0f1")
        
        # Top Bar
        top_frame = create_top_bar(self.root, "Feeding Schedule", user)
        tk.Button(top_frame, text="Close", bg="#95a5a6", fg="white",
                 command=self.root.destroy).pack(side="right", padx=10)
        
        # Main Frame
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Buttons
        btn_frame = create_button_frame(main_frame)
        
        create_button(btn_frame, "➕ Add Schedule", self.add_schedule, "#27ae60").pack(side="left", padx=5)
        create_button(btn_frame, "✅ Mark Complete", self.mark_complete, "#3498db").pack(side="left", padx=5)
        create_button(btn_frame, "🗑️ Delete Schedule", self.delete_schedule, "#e74c3c").pack(side="left", padx=5)
        create_button(btn_frame, "🔄 Refresh", self.load_schedules, "#95a5a6").pack(side="left", padx=5)
        
        # Filter
        filter_frame = tk.Frame(main_frame, bg="#ecf0f1")
        filter_frame.pack(fill="x", pady=10)
        
        tk.Label(filter_frame, text="Filter by Date:", font=("Arial", 11), bg="#ecf0f1").pack(side="left", padx=5)
        self.date_filter = tk.Entry(filter_frame, font=("Arial", 11), width=20)
        self.date_filter.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_filter.pack(side="left", padx=5)
        
        # Treeview
        columns = ("ID", "Animal", "Feed Time", "Food Type", "Quantity", "Staff", "Date", "Status")
        widths = [50, 150, 100, 120, 100, 120, 100, 100]
        self.tree = create_treeview(main_frame, columns, widths)
        
        # Load data
        self.load_schedules()
    
    def load_schedules(self):
        """Load all feeding schedules"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if db.connect():
            schedules = db.get_all_feeding_schedules()
            db.disconnect()
            
            for schedule in schedules:
                self.tree.insert("", "end", values=(
                    schedule['schedule_id'],
                    schedule['animal_name'],
                    format_time(schedule['feed_time']),
                    schedule['food_type'],
                    schedule['quantity'],
                    schedule['staff_name'],
                    format_date(schedule['schedule_date']),
                    schedule['status']
                ))
    
    def add_schedule(self):
        """Add new feeding schedule"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Feeding Schedule")
        dialog.geometry("450x500")
        dialog.configure(bg="#ecf0f1")
        
        tk.Label(dialog, text="Add Feeding Schedule", font=("Arial", 16, "bold"), bg="#ecf0f1").pack(pady=10)
        
        # Get data for dropdowns
        animal_names = get_animal_names()
        staff_names = get_staff_names()
        
        fields_frame = tk.Frame(dialog, bg="#ecf0f1")
        fields_frame.pack(pady=10, padx=20)
        
        tk.Label(fields_frame, text="Animal:", font=("Arial", 11), bg="#ecf0f1").grid(row=0, column=0, sticky="w", pady=5)
        animal_combo = ttk.Combobox(fields_frame, values=animal_names, font=("Arial", 11), width=28)
        animal_combo.grid(row=0, column=1, pady=5)
        
        tk.Label(fields_frame, text="Feed Time (HH:MM):", font=("Arial", 11), bg="#ecf0f1").grid(row=1, column=0, sticky="w", pady=5)
        time_entry = tk.Entry(fields_frame, font=("Arial", 11), width=30)
        time_entry.insert(0, "09:00")
        time_entry.grid(row=1, column=1, pady=5)
        
        tk.Label(fields_frame, text="Food Type:", font=("Arial", 11), bg="#ecf0f1").grid(row=2, column=0, sticky="w", pady=5)
        food_entry = tk.Entry(fields_frame, font=("Arial", 11), width=30)
        food_entry.grid(row=2, column=1, pady=5)
        
        tk.Label(fields_frame, text="Quantity:", font=("Arial", 11), bg="#ecf0f1").grid(row=3, column=0, sticky="w", pady=5)
        quantity_entry = tk.Entry(fields_frame, font=("Arial", 11), width=30)
        quantity_entry.grid(row=3, column=1, pady=5)
        
        tk.Label(fields_frame, text="Staff:", font=("Arial", 11), bg="#ecf0f1").grid(row=4, column=0, sticky="w", pady=5)
        staff_combo = ttk.Combobox(fields_frame, values=staff_names, font=("Arial", 11), width=28)
        staff_combo.grid(row=4, column=1, pady=5)
        
        tk.Label(fields_frame, text="Date (YYYY-MM-DD):", font=("Arial", 11), bg="#ecf0f1").grid(row=5, column=0, sticky="w", pady=5)
        date_entry = tk.Entry(fields_frame, font=("Arial", 11), width=30)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_entry.grid(row=5, column=1, pady=5)
        
        def save():
            animal_name = animal_combo.get()
            feed_time = time_entry.get()
            food_type = food_entry.get()
            quantity = quantity_entry.get()
            staff_name = staff_combo.get()
            schedule_date = date_entry.get()
            
            if not all([animal_name, feed_time, food_type, quantity, staff_name]):
                show_warning("Warning", "Please fill all fields")
                return
            
            if not validate_date(schedule_date):
                show_error("Error", "Invalid date format")
                return
            
            animal_id = get_animal_id_by_name(animal_name)
            staff_id = get_user_id_by_name(staff_name)
            
            if not animal_id or not staff_id:
                show_error("Error", "Invalid animal or staff selection")
                return
            
            if db.connect():
                if db.add_feeding_schedule(animal_id, feed_time, food_type, quantity, staff_id, schedule_date):
                    db.disconnect()
                    show_success("Success", "Feeding schedule added!")
                    dialog.destroy()
                    self.load_schedules()
                else:
                    db.disconnect()
        
        tk.Button(dialog, text="Save", bg="#27ae60", fg="white", 
                 font=("Arial", 12, "bold"), width=15, command=save).pack(pady=20)
    
    def mark_complete(self):
        """Mark schedule as completed"""
        values = get_selected_item(self.tree)
        if not values:
            return
        
        schedule_id = values[0]
        
        if db.connect():
            if db.update_feeding_status(schedule_id, "Completed"):
                db.disconnect()
                show_success("Success", "Marked as completed!")
                self.load_schedules()
            else:
                db.disconnect()
    
    def delete_schedule(self):
        """Delete selected schedule"""
        values = get_selected_item(self.tree)
        if not values:
            return
        
        if confirm_action("Confirm", "Delete this feeding schedule?"):
            if db.connect():
                if db.delete_feeding_schedule(values[0]):
                    db.disconnect()
                    show_success("Success", "Schedule deleted!")
                    self.load_schedules()
                else:
                    db.disconnect()


if __name__ == "__main__":
    test_user = {'user_id': 1, 'full_name': 'Admin', 'role': 'Admin'}
    root = tk.Tk()
    FeedingSchedule(root, test_user)
    root.mainloop()
