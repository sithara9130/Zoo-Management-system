"""
Enclosure Management for Zoo Management System
Save as: enclosure_management_integrated.py
"""

from common import *

class EnclosureManagement:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("Enclosure Management")
        self.root.geometry("1200x700")
        self.root.configure(bg="#ecf0f1")
        
        # Top Bar
        top_frame = create_top_bar(self.root, "Enclosure Management", user)
        tk.Button(top_frame, text="Close", bg="#95a5a6", fg="white",
                 command=self.root.destroy).pack(side="right", padx=10)
        
        # Main Frame
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Buttons
        btn_frame = create_button_frame(main_frame)
        
        create_button(btn_frame, "➕ Add Enclosure", self.add_enclosure, "#27ae60").pack(side="left", padx=5)
        create_button(btn_frame, "✏️ Edit Enclosure", self.edit_enclosure, "#3498db").pack(side="left", padx=5)
        create_button(btn_frame, "🗑️ Delete Enclosure", self.delete_enclosure, "#e74c3c").pack(side="left", padx=5)
        create_button(btn_frame, "🔄 Refresh", self.load_enclosures, "#95a5a6").pack(side="left", padx=5)
        
        # Treeview
        columns = ("ID", "Name", "Type", "Capacity", "Occupancy", "Status")
        widths = [100, 200, 150, 100, 100, 150]
        self.tree = create_treeview(main_frame, columns, widths)
        
        # Load data
        self.load_enclosures()
    
    def load_enclosures(self):
        """Load all enclosures"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if db.connect():
            enclosures = db.get_all_enclosures()
            db.disconnect()
            
            for enc in enclosures:
                self.tree.insert("", "end", values=(
                    enc['enclosure_id'],
                    enc['name'],
                    enc['type'],
                    enc['capacity'],
                    enc['current_occupancy'],
                    enc['condition_status']
                ))
    
    def add_enclosure(self):
        """Add new enclosure"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Enclosure")
        dialog.geometry("450x500")
        dialog.configure(bg="#ecf0f1")
        
        tk.Label(dialog, text="Add New Enclosure", font=("Arial", 16, "bold"), bg="#ecf0f1").pack(pady=10)
        
        fields_frame = tk.Frame(dialog, bg="#ecf0f1")
        fields_frame.pack(pady=10, padx=20)
        
        tk.Label(fields_frame, text="Enclosure ID:", font=("Arial", 11), bg="#ecf0f1").grid(row=0, column=0, sticky="w", pady=5)
        id_entry = tk.Entry(fields_frame, font=("Arial", 11), width=30)
        id_entry.grid(row=0, column=1, pady=5)
        
        tk.Label(fields_frame, text="Name:", font=("Arial", 11), bg="#ecf0f1").grid(row=1, column=0, sticky="w", pady=5)
        name_entry = tk.Entry(fields_frame, font=("Arial", 11), width=30)
        name_entry.grid(row=1, column=1, pady=5)
        
        tk.Label(fields_frame, text="Type:", font=("Arial", 11), bg="#ecf0f1").grid(row=2, column=0, sticky="w", pady=5)
        type_combo = ttk.Combobox(fields_frame, values=["Outdoor", "Indoor", "Aquatic", "Aviary"], 
                                  font=("Arial", 11), width=28)
        type_combo.grid(row=2, column=1, pady=5)
        
        tk.Label(fields_frame, text="Capacity:", font=("Arial", 11), bg="#ecf0f1").grid(row=3, column=0, sticky="w", pady=5)
        capacity_entry = tk.Entry(fields_frame, font=("Arial", 11), width=30)
        capacity_entry.grid(row=3, column=1, pady=5)
        
        tk.Label(fields_frame, text="Current Occupancy:", font=("Arial", 11), bg="#ecf0f1").grid(row=4, column=0, sticky="w", pady=5)
        occupancy_entry = tk.Entry(fields_frame, font=("Arial", 11), width=30)
        occupancy_entry.insert(0, "0")
        occupancy_entry.grid(row=4, column=1, pady=5)
        
        tk.Label(fields_frame, text="Condition Status:", font=("Arial", 11), bg="#ecf0f1").grid(row=5, column=0, sticky="w", pady=5)
        status_combo = ttk.Combobox(fields_frame, values=["Excellent", "Good", "Needs Repair", "Under Maintenance"], 
                                    font=("Arial", 11), width=28)
        status_combo.current(1)
        status_combo.grid(row=5, column=1, pady=5)
        
        def save():
            enclosure_id = id_entry.get().strip()
            name = name_entry.get().strip()
            enc_type = type_combo.get()
            capacity = capacity_entry.get().strip()
            occupancy = occupancy_entry.get().strip()
            status = status_combo.get()
            
            if not all([enclosure_id, name, enc_type, capacity]):
                show_warning("Warning", "Please fill all required fields")
                return
            
            try:
                capacity = int(capacity)
                occupancy = int(occupancy)
            except ValueError:
                show_error("Error", "Capacity and occupancy must be numbers")
                return
            
            if db.connect():
                if db.add_enclosure(enclosure_id, name, enc_type, capacity, occupancy, status):
                    db.disconnect()
                    show_success("Success", "Enclosure added successfully!")
                    dialog.destroy()
                    self.load_enclosures()
                else:
                    db.disconnect()
        
        tk.Button(dialog, text="Save", bg="#27ae60", fg="white", 
                 font=("Arial", 12, "bold"), width=15, command=save).pack(pady=20)
    
    def edit_enclosure(self):
        """Edit selected enclosure"""
        values = get_selected_item(self.tree)
        if not values:
            return
        
        enclosure_id = values[0]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Enclosure")
        dialog.geometry("450x500")
        dialog.configure(bg="#ecf0f1")
        
        tk.Label(dialog, text="Edit Enclosure", font=("Arial", 16, "bold"), bg="#ecf0f1").pack(pady=10)
        
        fields_frame = tk.Frame(dialog, bg="#ecf0f1")
        fields_frame.pack(pady=10, padx=20)
        
        tk.Label(fields_frame, text="Name:", font=("Arial", 11), bg="#ecf0f1").grid(row=0, column=0, sticky="w", pady=5)
        name_entry = tk.Entry(fields_frame, font=("Arial", 11), width=30)
        name_entry.insert(0, values[1])
        name_entry.grid(row=0, column=1, pady=5)
        
        tk.Label(fields_frame, text="Type:", font=("Arial", 11), bg="#ecf0f1").grid(row=1, column=0, sticky="w", pady=5)
        type_combo = ttk.Combobox(fields_frame, values=["Outdoor", "Indoor", "Aquatic", "Aviary"], 
                                  font=("Arial", 11), width=28)
        type_combo.set(values[2])
        type_combo.grid(row=1, column=1, pady=5)
        
        tk.Label(fields_frame, text="Capacity:", font=("Arial", 11), bg="#ecf0f1").grid(row=2, column=0, sticky="w", pady=5)
        capacity_entry = tk.Entry(fields_frame, font=("Arial", 11), width=30)
        capacity_entry.insert(0, values[3])
        capacity_entry.grid(row=2, column=1, pady=5)
        
        tk.Label(fields_frame, text="Current Occupancy:", font=("Arial", 11), bg="#ecf0f1").grid(row=3, column=0, sticky="w", pady=5)
        occupancy_entry = tk.Entry(fields_frame, font=("Arial", 11), width=30)
        occupancy_entry.insert(0, values[4])
        occupancy_entry.grid(row=3, column=1, pady=5)
        
        tk.Label(fields_frame, text="Condition Status:", font=("Arial", 11), bg="#ecf0f1").grid(row=4, column=0, sticky="w", pady=5)
        status_combo = ttk.Combobox(fields_frame, values=["Excellent", "Good", "Needs Repair", "Under Maintenance"], 
                                    font=("Arial", 11), width=28)
        status_combo.set(values[5])
        status_combo.grid(row=4, column=1, pady=5)
        
        def update():
            if db.connect():
                if db.update_enclosure(enclosure_id, name_entry.get(), type_combo.get(), 
                                      capacity_entry.get(), occupancy_entry.get(), status_combo.get()):
                    db.disconnect()
                    show_success("Success", "Enclosure updated successfully!")
                    dialog.destroy()
                    self.load_enclosures()
                else:
                    db.disconnect()
        
        tk.Button(dialog, text="Update", bg="#3498db", fg="white", 
                 font=("Arial", 12, "bold"), width=15, command=update).pack(pady=20)
    
    def delete_enclosure(self):
        """Delete selected enclosure"""
        values = get_selected_item(self.tree)
        if not values:
            return
        
        if confirm_action("Confirm", f"Delete enclosure '{values[1]}'?"):
            if db.connect():
                if db.delete_enclosure(values[0]):
                    db.disconnect()
                    show_success("Success", "Enclosure deleted successfully!")
                    self.load_enclosures()
                else:
                    db.disconnect()


if __name__ == "__main__":
    test_user = {'user_id': 1, 'full_name': 'Admin', 'role': 'Admin'}
    root = tk.Tk()
    EnclosureManagement(root, test_user)
    root.mainloop()
