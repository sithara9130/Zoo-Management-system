"""
Admin Dashboard for Zoo Management System
Save as: admin_dashboard_integrated.py
"""

from common import *

class AdminDashboard:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("Zoo Management System - Admin Dashboard")
        self.root.geometry("1200x700")
        self.root.configure(bg="#ecf0f1")
        
        # Top Bar
        top_frame = create_top_bar(self.root, "Admin Dashboard", user)
        
        tk.Button(top_frame, text="Logout", 
                 bg="#e74c3c", fg="white",
                 font=("Arial", 11),
                 command=lambda: NavigationManager.logout(self.root)).pack(side="right", padx=10)
        
        # Main Container
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(fill="both", expand=True)
        
        # Left Menu
        self.create_menu(main_frame)
        
        # Content Area
        content_frame = tk.Frame(main_frame, bg="#ecf0f1")
        content_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(content_frame, text="Quick Statistics", 
                font=("Arial", 18, "bold"),
                bg="#ecf0f1").pack(pady=10)
        
        # Stats Cards
        self.create_stats(content_frame)
        
        # Notifications
        self.create_notifications(content_frame)
    
    def create_menu(self, parent):
        """Create left navigation menu"""
        menu_frame = tk.Frame(parent, bg="#2c3e50", width=250)
        menu_frame.pack(side="left", fill="y")
        
        tk.Label(menu_frame, text="Navigation", 
                font=("Arial", 14, "bold"),
                bg="#2c3e50", fg="white").pack(pady=20)
        
        menu_items = [
            ("🏠 Dashboard", lambda: None),
            ("🦁 Animal Records", lambda: NavigationManager.open_animal_records(self.user, self.root)),
            ("🍖 Feeding Schedule", lambda: NavigationManager.open_feeding_schedule(self.user, self.root)),
            ("💊 Health Updates", lambda: NavigationManager.open_health_updates(self.user, self.root)),
            ("🏛️ Enclosures", lambda: NavigationManager.open_enclosure_management(self.user, self.root)),
            ("👥 Staff Management", lambda: NavigationManager.open_staff_management(self.user, self.root))
        ]
        
        for text, command in menu_items:
            tk.Button(menu_frame, text=text, 
                     font=("Arial", 12), 
                     bg="#34495e", fg="white",
                     width=25, height=2, 
                     relief="flat",
                     anchor="w",
                     command=command).pack(pady=2, padx=5)
    
    def create_stats(self, parent):
        """Create statistics cards"""
        stats_frame = tk.Frame(parent, bg="#ecf0f1")
        stats_frame.pack(fill="x", pady=10)
        
        # Get stats from database
        if db.connect():
            stats = db.get_dashboard_stats()
            db.disconnect()
        else:
            stats = {'total_animals': 0, 'total_staff': 0, 'total_enclosures': 0}
        
        # Create stat cards
        self.create_stat_card(stats_frame, "🦁 Total Animals", 
                             stats['total_animals'], "#3498db")
        self.create_stat_card(stats_frame, "👥 Total Staff", 
                             stats['total_staff'], "#2ecc71")
        self.create_stat_card(stats_frame, "🏛️ Total Enclosures", 
                             stats['total_enclosures'], "#e67e22")
    
    def create_stat_card(self, parent, title, value, color):
        """Create individual stat card"""
        card = tk.Frame(parent, bg=color, width=200, height=120)
        card.pack(side="left", padx=10, fill="both", expand=True)
        
        tk.Label(card, text=str(value), 
                font=("Arial", 36, "bold"), 
                bg=color, fg="white").pack(expand=True)
        tk.Label(card, text=title, 
                font=("Arial", 12), 
                bg=color, fg="white").pack(pady=5)
    
    def create_notifications(self, parent):
        """Create notifications section"""
        notif_frame = tk.LabelFrame(parent, text="📢 Recent Activity", 
                                    font=("Arial", 14, "bold"), 
                                    bg="#ecf0f1")
        notif_frame.pack(fill="both", expand=True, pady=20)
        
        notif_text = tk.Text(notif_frame, height=10, font=("Arial", 11), 
                            bg="white", wrap="word", relief="flat")
        notif_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Sample notifications
        notifications = [
            f"• Welcome back, {self.user['full_name']}!",
            "• System is running smoothly",
            "• All enclosures are in good condition",
            "• No urgent health updates",
            "• Feeding schedules are up to date"
        ]
        
        for notif in notifications:
            notif_text.insert("end", notif + "\n\n")
        
        notif_text.config(state="disabled")


if __name__ == "__main__":
    # Test user
    test_user = {
        'user_id': 1,
        'username': 'admin',
        'full_name': 'Administrator',
        'role': 'Admin'
    }
    root = tk.Tk()
    AdminDashboard(root, test_user)
    root.mainloop()
