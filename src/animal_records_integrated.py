"""
Animal Records Management for Zoo Management System
Save as: animal_records_integrated.py
"""

from common import *

class AnimalRecords:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("Animal Records Management")
        self.root.geometry("1200x700")
        self.root.configure(bg="#ecf0f1")
        
        # Top Bar
        top_frame = create_top_bar(self.root, "Animal Records Management", user)
        tk.Button(top_frame, text="Close", bg="#95a5a6", fg="white",
                 command=self.root.destroy).pack(side="right", padx=10)
        
        # Main Frame
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Buttons
        btn_frame = create_button_frame(main_frame)
        
        create_button(btn_frame, "➕ Add Animal", self.add_animal, "#27ae60").pack(side="left", padx=5)
        create_button(btn_frame, "✏️ Edit Animal", self.edit_animal, "#3498db").pack(side="left", padx=5)
        create_button(btn_frame, "🗑️ Delete Animal", self.delete_animal, "#e74c3c").pack(side="left", padx=5)
        create_button(btn_frame, "🔄 Refresh", self.load_animals, "#95a5a6").pack(side="left", padx=5)
        
        # Search
        search_frame = tk.Frame(main_frame, bg="#ecf0f1")
        search_frame.pack(fill="x", pady=10)
        
        tk.Label(search_frame, text="Search:", font=("Arial", 11), bg="#ecf0f1").pack(side="left", padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Arial", 11), width=30)
        self.search_entry.pack(side="left", padx=5)
        create_button(search_frame, "🔍 Search", self.search_animals, "#3498db", width=10).pack(side="left", padx=5)
        
        # Treeview
        columns = ("ID", "Name", "Species", "Age", "Gender", "Enclosure", "Health Status", "Arrival Date")
        widths = [50, 120, 120, 60, 80, 100, 120, 120]
        self.tree = create_treeview(main_frame, columns, widths)
        
        # Load data
        self.load_animals()
    
    def load_animals(self):
        """Load all animals from database"""
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if db.connect():
            animals = db.get_all_animals()
            db.disconnect()
            
            for animal in animals:
                self.tree.insert("", "end", values=(
                    animal['animal_id'],
                    animal['name'],
                    animal['species'],
                    animal['age'],
                    animal['gender'],
                    animal['enclosure_id'],
                    animal['health_status'],
                    format_date(animal['arrival_date'])
                ))
    
    def search_animals(self):
        """Search animals"""
        search_term = self.search_entry.get().strip()
        if not search_term:
            self.load_animals()
            return
        
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if db.connect():
            animals = db.search_animals(search_term)
            db.disconnect()
            
            for animal in animals:
                self.tree.insert("", "end", values=(
                    animal['animal_id'],
                    animal['name'],
                    animal['species'],
                    animal['age'],
                    animal['gender'],
                    animal['enclosure_id'],
                    animal['health_status'],
                    format_date(animal['arrival_date'])
                ))
    
    def add_animal(self):
        """Add new animal"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Animal")
        dialog.geometry("450x550")
        dialog.configure(bg="#ecf0f1")
        
        tk.Label(dialog, text="Add New Animal", font=("Arial", 16, "bold"), bg="#ecf0f1").pack(pady=10)
        
        # Get enclosure IDs
        enclosure_ids = get_enclosure_ids()
        
        # Fields
        fields_frame = tk.Frame(dialog, bg="#ecf0f1")
        fields_frame.pack(pady=10, padx=20)
        
        tk.Label(fields_frame, text="Name:", font=("Arial", 11), bg="#ecf0f1").grid(row=0, column=0, sticky="w", pady=5)
        name_entry = tk.Entry(fields_frame, font=("Arial", 11), width=30)
        name_entry.grid(row=0, column=1, pady=5)
        
        tk.Label(fields_frame, text="Species:", font=("Arial", 11), bg="#ecf0f1").grid(row=1, column=0, sticky="w", pady=5)
        species_entry = tk.Entry(fields_frame, font=("Arial", 11), width=30)
        species_entry.grid(row=1, column=1, pady=5)
        
        tk.Label(fields_frame, text="Age:", font=("Arial", 11), bg="#ecf0f1").grid(row=2, column=0, sticky="w", pady=5)
        age_entry = tk.Entry(fields_frame, font=("Arial", 11), width=30)
        age_entry.grid(row=2, column=1, pady=5)
        
        tk.Label(fields_frame, text="Gender:", font=("Arial", 11), bg="#ecf0f1").grid(row=3, column=0, sticky="w", pady=5)
        gender_combo = ttk.Combobox(fields_frame, values=["Male", "Female"], font=("Arial", 11), width=28)
        gender_combo.grid(row=3, column=1, pady=5)
        
        tk.Label(fields_frame, text="Enclosure ID:", font=("Arial", 11), bg="#ecf0f1").grid(row=4, column=0, sticky="w", pady=5)
        enclosure_combo = ttk.Combobox(fields_frame, values=enclosure_ids, font=("Arial", 11), width=28)
        enclosure_combo.grid(row=4, column=1, pady=5)
        
        tk.Label(fields_frame, text="Health Status:", font=("Arial", 11), bg="#ecf0f1").grid(row=5, column=0, sticky="w", pady=5)
        health_entry = tk.Entry(fields_frame, font=("Arial", 11), width=30)
        health_entry.insert(0, "Healthy")
        health_entry.grid(row=5, column=1, pady=5)
        
        tk.Label(fields_frame, text="Arrival Date:", font=("Arial", 11), bg="#ecf0f1").grid(row=6, column=0, sticky="w", pady=5)
        date_entry = tk.Entry(fields_frame, font=("Arial", 11), width=30)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_entry.grid(row=6, column=1, pady=5)
        
        def save():
            name = name_entry.get().strip()
            species = species_entry.get().strip()
            age = age_entry.get().strip()
            gender = gender_combo.get()
            enclosure_id = enclosure_combo.get()
            health_status = health_entry.get().strip()
            arrival_date = date_entry.get().strip()
            
            if not all([name, species, age, gender, enclosure_id]):
                show_warning("Warning", "Please fill all required fields")
                return
            
            if not validate_date(arrival_date):
                show_error("Error", "Invalid date format. Use YYYY-MM-DD")
                return
            
            if db.connect():
                if db.add_animal(name, species, age, gender, enclosure_id, health_status, arrival_date):
                    db.disconnect()
                    show_success("Success", "Animal added successfully!")
                    dialog.destroy()
                    self.load_animals()
                else:
                    db.disconnect()
        
        tk.Button(dialog, text="Save", bg="#27ae60", fg="white", 
                 font=("Arial", 12, "bold"), width=15, command=save).pack(pady=20)
    
    def edit_animal(self):
        """Edit selected animal"""
        values = get_selected_item(self.tree)
        if not values:
            return
        
        animal_id = values[0]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Animal")
        dialog.geometry("450x550")
        dialog.configure(bg="#ecf0f1")
        
        tk.Label(dialog, text="Edit Animal", font=("Arial", 16, "bold"), bg="#ecf0f1").pack(pady=10)
        
        enclosure_ids = get_enclosure_ids()
        
        fields_frame = tk.Frame(dialog, bg="#ecf0f1")
        fields_frame.pack(pady=10, padx=20)
        
        tk.Label(fields_frame, text="Name:", font=("Arial", 11), bg="#ecf0f1").grid(row=0, column=0, sticky="w", pady=5)
        name_entry = tk.Entry(fields_frame, font=("Arial", 11), width=30)
        name_entry.insert(0, values[1])
        name_entry.grid(row=0, column=1, pady=5)
        
        tk.Label(fields_frame, text="Species:", font=("Arial", 11), bg="#ecf0f1").grid(row=1, column=0, sticky="w", pady=5)
        species_entry = tk.Entry(fields_frame, font=("Arial", 11), width=30)
        species_entry.insert(0, values[2])
        species_entry.grid(row=1, column=1, pady=5)
        
        tk.Label(fields_frame, text="Age:", font=("Arial", 11), bg="#ecf0f1").grid(row=2, column=0, sticky="w", pady=5)
        age_entry = tk.Entry(fields_frame, font=("Arial", 11), width=30)
        age_entry.insert(0, values[3])
        age_entry.grid(row=2, column=1, pady=5)
        
        tk.Label(fields_frame, text="Gender:", font=("Arial", 11), bg="#ecf0f1").grid(row=3, column=0, sticky="w", pady=5)
        gender_combo = ttk.Combobox(fields_frame, values=["Male", "Female"], font=("Arial", 11), width=28)
        gender_combo.set(values[4])
        gender_combo.grid(row=3, column=1, pady=5)
        
        tk.Label(fields_frame, text="Enclosure ID:", font=("Arial", 11), bg="#ecf0f1").grid(row=4, column=0, sticky="w", pady=5)
        enclosure_combo = ttk.Combobox(fields_frame, values=enclosure_ids, font=("Arial", 11), width=28)
        enclosure_combo.set(values[5])
        enclosure_combo.grid(row=4, column=1, pady=5)
        
        tk.Label(fields_frame, text="Health Status:", font=("Arial", 11), bg="#ecf0f1").grid(row=5, column=0, sticky="w", pady=5)
        health_entry = tk.Entry(fields_frame, font=("Arial", 11), width=30)
        health_entry.insert(0, values[6])
        health_entry.grid(row=5, column=1, pady=5)
        
        def update():
            if db.connect():
                if db.update_animal(animal_id, name_entry.get(), species_entry.get(), 
                                   age_entry.get(), gender_combo.get(), 
                                   enclosure_combo.get(), health_entry.get()):
                    db.disconnect()
                    show_success("Success", "Animal updated successfully!")
                    dialog.destroy()
                    self.load_animals()
                else:
                    db.disconnect()
        
        tk.Button(dialog, text="Update", bg="#3498db", fg="white", 
                 font=("Arial", 12, "bold"), width=15, command=update).pack(pady=20)
    
    def delete_animal(self):
        """Delete selected animal"""
        values = get_selected_item(self.tree)
        if not values:
            return
        
        if confirm_action("Confirm", f"Delete animal '{values[1]}'?"):
            if db.connect():
                if db.delete_animal(values[0]):
                    db.disconnect()
                    show_success("Success", "Animal deleted successfully!")
                    self.load_animals()
                else:
                    db.disconnect()


if __name__ == "__main__":
    test_user = {'user_id': 1, 'full_name': 'Admin', 'role': 'Admin'}
    root = tk.Tk()
    AnimalRecords(root, test_user)
    root.mainloop()
