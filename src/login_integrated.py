"""
Login Page for Zoo Management System
Save as: login_integrated.py
"""

from common import *

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Zoo Management System - Login")
        self.root.geometry("500x600")
        self.root.configure(bg="#2c3e50")
        
        # Center window
        self.center_window()
        
        # Main Frame
        frame = tk.Frame(self.root, bg="#2c3e50")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo/Title
        tk.Label(frame, text="🦁", 
                font=("Arial", 48), 
                bg="#2c3e50").pack(pady=10)
        
        tk.Label(frame, text="Zoo Management System", 
                font=("Arial", 24, "bold"), 
                bg="#2c3e50", fg="white").pack(pady=10)
        
        tk.Label(frame, text="Version 1.0.0", 
                font=("Arial", 10), 
                bg="#2c3e50", fg="#95a5a6").pack(pady=5)
        
        # Login Form
        tk.Label(frame, text="Login", 
                font=("Arial", 18, "bold"), 
                bg="#2c3e50", fg="white").pack(pady=20)
        
        # Username
        tk.Label(frame, text="Username:", 
                font=("Arial", 12), 
                bg="#2c3e50", fg="white").pack(pady=5)
        self.username_entry = tk.Entry(frame, font=("Arial", 12), width=30)
        self.username_entry.pack(pady=5)
        
        # Password
        tk.Label(frame, text="Password:", 
                font=("Arial", 12), 
                bg="#2c3e50", fg="white").pack(pady=5)
        self.password_entry = tk.Entry(frame, font=("Arial", 12), width=30, show="●")
        self.password_entry.pack(pady=5)
        
        # Buttons
        btn_frame = tk.Frame(frame, bg="#2c3e50")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Login", 
                 font=("Arial", 12, "bold"), 
                 bg="#27ae60", fg="white",
                 width=12, height=2,
                 command=self.login).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="Reset", 
                 font=("Arial", 12, "bold"), 
                 bg="#e74c3c", fg="white",
                 width=12, height=2,
                 command=self.reset).pack(side="left", padx=5)
        
        # Enter key binding
        self.root.bind('<Return>', lambda e: self.login())
        

    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def reset(self):
        """Clear input fields"""
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.username_entry.focus()
    
    def login(self):
        """Handle login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Validation
        if not username or not password:
            show_warning("Warning", "Please enter both username and password")
            return
        
        # Connect to database
        if not db.connect():
            show_error("Connection Error", "Could not connect to database")
            return
        
        # Validate credentials
        user = db.validate_login(username, password)
        db.disconnect()
        
        if user:
            # Successful login
            if user['role'] == 'Admin':
                NavigationManager.open_admin_dashboard(user, self.root)
            else:
                NavigationManager.open_staff_dashboard(user, self.root)
        else:
            show_error("Login Failed", "Invalid username or password")
            self.password_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    LoginPage(root)
    root.mainloop()
