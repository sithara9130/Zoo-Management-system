"""
Health Updates for Zoo Management System
Save as: health_updates_integrated.py
"""

from common import *
from tkinter import scrolledtext

class HealthUpdates:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("Health Updates")
        self.root.geometry("1200x700")
        self.root.configure(bg="#ecf0f1")
        
        # Top Bar
        top_frame = create_top_bar(self.root, "Health Updates", user)
        tk.Button(top_frame, text="Close", bg="#95a5a6", fg="white",
                 command=self.root.destroy).pack(side="right", padx=10)
        
        # Main Frame
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Buttons
        btn_frame = create_button_frame(main_frame)
        
        create_button(btn_frame, "➕ Add Record", self.add_record, "#27ae60", width=18).pack(side="left", padx=5)
        create_button(btn_frame, "👁️ View Details", self.view_details, "#3498db", width=18).pack(side="left", padx=5)
        create_button(btn_frame, "🗑️ Delete Record", self.delete_record, "#e74c3c", width=18).pack(side="left", padx=5)
        create_button(btn_frame, "🔄 Refresh", self.load_records, "#95a5a6", width=18).pack(side="left", padx=5)
        
        # Treeview
        columns = ("ID", "Animal", "Check Date", "Condition", "Treatment", "Vet", "Next Checkup")
        widths = [50, 150, 100, 150, 150, 120, 110]
        self.tree = create_treeview(main_frame, columns, widths)
        
        # Load data
        self.load_records()
    
    def load_records(self):
        """Load all health records"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if db.connect():
            records = db.get_all_health_records()
            db.disconnect()
            
            for record in records:
                self.tree.insert("", "end", values=(
                    record['record_id'],
                    record['animal_name'],
                    format_date(record['check_date']),
                    record['condition_desc'][:30] + "..." if len(record['condition_desc']) > 30 else record['condition_desc'],
                    record['treatment'][:30] + "..." if len(record['treatment']) > 30 else record['treatment'],
                    record['vet_name'],
                    format_date(record['next_checkup'])
                ))
    
    def add_record(self):
        """Add new health record"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Health Record")
        dialog.geometry("500x650")
        dialog.configure(bg="#ecf0f1")
        
        tk.Label(dialog, text="Add Health Record", font=("Arial", 16, "bold"), bg="#ecf0f1").pack(pady=10)
        
        animal_names = get_animal_names()
        
        # Scrollable frame
        canvas = tk.Canvas(dialog, bg="#ecf0f1")
        scrollbar = tk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ecf0f1")
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Animal selection
        tk.Label(scrollable_frame, text="Animal:", font=("Arial", 11), bg="#ecf0f1").pack(pady=5)
        animal_combo = ttk.Combobox(scrollable_frame, values=animal_names, font=("Arial", 11), width=35)
        animal_combo.pack(pady=5)
        
        # Check date
        tk.Label(scrollable_frame, text="Check Date (YYYY-MM-DD):", font=("Arial", 11), bg="#ecf0f1").pack(pady=5)
        date_entry = tk.Entry(scrollable_frame, font=("Arial", 11), width=38)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_entry.pack(pady=5)
        
        # Condition
        tk.Label(scrollable_frame, text="Condition Description:", font=("Arial", 11), bg="#ecf0f1").pack(pady=5)
        condition_text = scrolledtext.ScrolledText(scrollable_frame, font=("Arial", 11), width=35, height=4)
        condition_text.pack(pady=5)
        
        # Treatment
        tk.Label(scrollable_frame, text="Treatment:", font=("Arial", 11), bg="#ecf0f1").pack(pady=5)
        treatment_text = scrolledtext.ScrolledText(scrollable_frame, font=("Arial", 11), width=35, height=4)
        treatment_text.pack(pady=5)
        
        # Vet notes
        tk.Label(scrollable_frame, text="Vet Notes:", font=("Arial", 11), bg="#ecf0f1").pack(pady=5)
        notes_text = scrolledtext.ScrolledText(scrollable_frame, font=("Arial", 11), width=35, height=4)
        notes_text.pack(pady=5)
        
        # Vet name
        tk.Label(scrollable_frame, text="Vet Name:", font=("Arial", 11), bg="#ecf0f1").pack(pady=5)
        vet_entry = tk.Entry(scrollable_frame, font=("Arial", 11), width=38)
        vet_entry.pack(pady=5)
        
        # Next checkup
        tk.Label(scrollable_frame, text="Next Checkup (YYYY-MM-DD):", font=("Arial", 11), bg="#ecf0f1").pack(pady=5)
        next_entry = tk.Entry(scrollable_frame, font=("Arial", 11), width=38)
        next_entry.pack(pady=5)
        
        def save():
            animal_name = animal_combo.get()
            check_date = date_entry.get()
            condition = condition_text.get("1.0", "end-1c")
            treatment = treatment_text.get("1.0", "end-1c")
            vet_notes = notes_text.get("1.0", "end-1c")
            vet_name = vet_entry.get()
            next_checkup = next_entry.get()
            
            if not all([animal_name, condition, treatment, vet_name]):
                show_warning("Warning", "Please fill all required fields")
                return
            
            if not validate_date(check_date) or not validate_date(next_checkup):
                show_error("Error", "Invalid date format")
                return
            
            animal_id = get_animal_id_by_name(animal_name)
            if not animal_id:
                show_error("Error", "Invalid animal selection")
                return
            
            if db.connect():
                if db.add_health_record(animal_id, check_date, condition, treatment, vet_notes, vet_name, next_checkup):
                    db.disconnect()
                    show_success("Success", "Health record added!")
                    dialog.destroy()
                    self.load_records()
                else:
                    db.disconnect()
        
        tk.Button(scrollable_frame, text="Save", bg="#27ae60", fg="white", 
                 font=("Arial", 12, "bold"), width=15, command=save).pack(pady=20)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")
    
    def view_details(self):
        """View full details of selected record"""
        values = get_selected_item(self.tree)
        if not values:
            return
        
        record_id = values[0]
        
        # Get full record from database
        if db.connect():
            query = "SELECT * FROM health_records WHERE record_id = %s"
            result = db.execute_query(query, (record_id,), fetch=True)
            db.disconnect()
            
            if result:
                record = result[0]
                
                detail_window = tk.Toplevel(self.root)
                detail_window.title("Health Record Details")
                detail_window.geometry("600x500")
                detail_window.configure(bg="#ecf0f1")
                
                tk.Label(detail_window, text="Health Record Details", 
                        font=("Arial", 16, "bold"), bg="#ecf0f1").pack(pady=10)
                
                text = scrolledtext.ScrolledText(detail_window, font=("Arial", 11), wrap="word")
                text.pack(padx=20, pady=10, fill="both", expand=True)
                
                details = f"""Animal: {values[1]}
Check Date: {format_date(record['check_date'])}

Condition Description:
{record['condition_desc']}

Treatment:
{record['treatment']}

Vet Notes:
{record['vet_notes']}

Vet Name: {record['vet_name']}
Next Checkup: {format_date(record['next_checkup'])}
"""
                
                text.insert("1.0", details)
                text.config(state="disabled")
    
    def delete_record(self):
        """Delete selected health record"""
        values = get_selected_item(self.tree)
        if not values:
            return
        
        if confirm_action("Confirm", "Delete this health record?"):
            if db.connect():
                if db.delete_health_record(values[0]):
                    db.disconnect()
                    show_success("Success", "Record deleted!")
                    self.load_records()
                else:
                    db.disconnect()


if __name__ == "__main__":
    test_user = {'user_id': 1, 'full_name': 'Admin', 'role': 'Admin'}
    root = tk.Tk()
    HealthUpdates(root, test_user)
    root.mainloop()
