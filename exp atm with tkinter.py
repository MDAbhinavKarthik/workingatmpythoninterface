import tkinter as tk
from tkinter import messagebox
import random
import sqlite3
import datetime

class User:
    def __init__(self, user_id, pin, name, balance=0, email='', phone_number='', address='', details=None):
        if details is None:
            details = ['', '', '']
        self.user_id = user_id
        self.pin = pin
        self.name = name
        self.balance = balance
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.details = details
        self.transactions = []

    def display_balance(self):
        return f"Current Balance: ₹{self.balance}"

class ATM:
    def __init__(self, root): #constructor
        self.root = root
        self.root.title("ATM Application")
        self.current_user = None
        self._initialize_database()
        self.create_main_menu()

    def _connect_db(self):
        return sqlite3.connect('atm_database.db')

    def _initialize_database(self):
        conn = self._connect_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                pin TEXT,
                name TEXT,
                balance REAL,
                email TEXT,
                phone_number TEXT,
                address TEXT,
                details TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                amount REAL,
                timestamp TEXT,
                type TEXT,
                recipient_user_id TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')
        
        conn.commit()
        conn.close()

    def create_main_menu(self):
        self.clear_window()
        
        font_settings = ("Helvetica", 25)
        font_headings = ("Helvetica",18)
        md_headings = ("Helvetica",40)
        
        tk.Label(self.root, text=f"༺ ϻᴅ's A.T.M ༻", fg='darkblue', font=md_headings).pack(pady=30)
        
        login_button = tk.Button(self.root, text="Login", command=self.show_login, bg="lightblue", width=15, font=font_headings)
        login_button.pack(pady=10)
        
        register_button = tk.Button(self.root, text="Register", command=self.show_register, bg="lightgreen", width=15, font=font_headings)
        register_button.pack(pady=10)
        
        quit_button = tk.Button(self.root, text="Quit", command=self.root.quit, bg="red", width=15, font=font_headings)
        quit_button.pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_register(self):
        self.clear_window()
        
        font_settings = ("Helvetica", 25)
        font_headings = ("Helvetica",18)
        md_headings = ("Helvetica",35)
        
        tk.Label(self.root, text="Register with  ϻᴅ's A.T.M ༻ ", fg='darkblue', font=md_headings).pack(pady=10)
        tk.Label(self.root, text="Your financial Partner", font=font_headings).pack(pady=10)

        tk.Label(self.root, text="First Name:", font=font_headings).pack()
        first_name_entry = tk.Entry(self.root, font=font_headings)
        first_name_entry.pack()

        tk.Label(self.root, text="Last Name:", font=font_headings).pack()
        last_name_entry = tk.Entry(self.root, font=font_headings)
        last_name_entry.pack()

        tk.Label(self.root, text="Email:", font=font_headings).pack()
        email_entry = tk.Entry(self.root, font=font_headings)
        email_entry.pack()

        tk.Label(self.root, text="Phone Number:", font=font_headings).pack()
        phone_number_entry = tk.Entry(self.root, font=font_headings)
        phone_number_entry.pack()

        tk.Label(self.root, text="Address:", font=font_headings).pack()
        address_entry = tk.Entry(self.root, font=font_headings)
        address_entry.pack()

        tk.Label(self.root, text="Password:", font=font_headings).pack()
        password_entry = tk.Entry(self.root, show='*', font=font_headings)
        password_entry.pack()

        tk.Label(self.root, text="Confirm Password:", font=font_headings).pack()
        confirm_password_entry = tk.Entry(self.root, show='*', font=font_headings)
        confirm_password_entry.pack()

        def register_user():
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            email = email_entry.get()
            phone_number = phone_number_entry.get()
            address = address_entry.get()
            password = password_entry.get()
            confirm_password = confirm_password_entry.get()

            if password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match!")
                return

            user_id = str(random.randint(1000, 9999))
            while self.get_user(user_id):
                user_id = str(random.randint(1000, 9999))
            
            self.create_account(user_id, f"{first_name} {last_name}", password, 100, email, phone_number, address)
            messagebox.showinfo("Success", f"Registration successful! Your User ID is {user_id}")
            self.create_main_menu()

        tk.Button(self.root, text="Register", command=register_user, font=font_settings).pack(pady=10)
        tk.Button(self.root, text="Back to Menu", command=self.create_main_menu, font=font_settings).pack(pady=10)

    def show_login(self):
        self.clear_window()
        
        font_settings = ("Helvetica", 25)
        font_headings = ("Helvetica",18)
        md_headings = ("Helvetica",35)

        tk.Label(self.root, text=f"Login to  ϻᴅ's A.T.M ༻", fg='darkblue', font=md_headings).pack(pady=10)

        tk.Label(self.root, text="User ID:", font=font_headings).pack()
        user_id_entry = tk.Entry(self.root, font=font_headings)
        user_id_entry.pack()

        tk.Label(self.root, text="Password:", font=font_headings).pack()
        password_entry = tk.Entry(self.root, show='*', font=font_headings)
        password_entry.pack()

        def login_user():
            user_id = user_id_entry.get()
            password = password_entry.get()
            if self.authenticate_user(user_id, password):
                self.current_user = user_id
                self.show_account_menu()
            else:
                messagebox.showerror("Error", "Invalid User ID or Password!")

        tk.Button(self.root, text="Login", command=login_user, font=font_settings).pack(pady=10)
        tk.Button(self.root, text="Back to Menu", command=self.create_main_menu, font=font_settings).pack(pady=10)

    def show_account_menu(self):
        self.clear_window()
        
        font_settings = ("Helvetica", 25)
        font_headings = ("Helvetica",18)
        md_headings = ("Helvetica",35)
        
        tk.Label(self.root, text=f" Navigate Your Finances with Confidence ", fg='darkblue', font=md_headings).pack(pady=10)

        tk.Button(self.root, text="Transfer", command=self.show_transfer, bg="lightblue", width=15, font=font_headings).pack(pady=10)
        tk.Button(self.root, text="Withdraw", command=self.show_withdraw, bg="lightblue", width=15, font=font_headings).pack(pady=10)
        tk.Button(self.root, text="Deposit", command=self.show_deposit, bg="lightblue", width=15, font=font_headings).pack(pady=10)
        tk.Button(self.root, text="Check Balance", command=self.show_check_balance, bg="lightblue", width=15, font=font_headings).pack(pady=10)
        tk.Button(self.root, text="Change Password", command=self.show_change_password, bg="lightblue", width=15, font=font_headings).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.create_main_menu, bg="red", width=15, font=font_headings).pack(pady=10)

    def show_transfer(self):
        self.clear_window()
        
        font_settings = ("Helvetica", 25)
        font_headings = ("Helvetica",18)
        md_headings = ("Helvetica",35)
        
        tk.Label(self.root, text="Transfer with  ϻᴅ's A.T.M ༻", font=md_headings).pack(pady=10)
        tk.Label(self.root, text=f"Secure Your Transactions", font=font_settings).pack(pady=10)

        tk.Label(self.root, text="Recipient User ID:", font=font_headings).pack()
        recipient_id_entry = tk.Entry(self.root, font=font_headings)
        recipient_id_entry.pack()

        tk.Label(self.root, text="Amount:", font=font_headings).pack()
        amount_entry = tk.Entry(self.root, font=font_headings)
        amount_entry.pack()

        tk.Label(self.root, text="Password:", font=font_headings).pack()
        password_entry = tk.Entry(self.root, show='*', font=font_headings)
        password_entry.pack()

        def transfer_money():
            recipient_id = recipient_id_entry.get()
            amount = float(amount_entry.get())
            password = password_entry.get()
            if self.authenticate_user(self.current_user, password):
                messagebox.showinfo("Info", self.perform_transfer(amount, recipient_id))
                self.show_account_menu()
            else:
                messagebox.showerror("Error", "Invalid Password!")

        tk.Button(self.root, text="Transfer", command=transfer_money, font=font_settings).pack(pady=10)
        tk.Button(self.root, text="Back to Menu", command=self.show_account_menu, font=font_settings).pack(pady=10)

    def show_withdraw(self):
        self.clear_window()
        
        font_settings = ("Helvetica", 25)
        font_headings = ("Helvetica",18)
        md_headings = ("Helvetica",35)
        
        tk.Label(self.root, text=f"Withdraw from  ϻᴅ's A.T.M ༻", font=md_headings).pack(pady=10)

        tk.Label(self.root, text="Amount:", font=font_headings).pack()
        amount_entry = tk.Entry(self.root, font=font_headings)
        amount_entry.pack()

        tk.Label(self.root, text="Password:", font=font_headings).pack()
        password_entry = tk.Entry(self.root, show='*', font=font_headings)
        password_entry.pack()

        def withdraw_money():
            amount = float(amount_entry.get())
            password = password_entry.get()
            if self.authenticate_user(self.current_user, password):
                messagebox.showinfo("Info", self.perform_withdrawal(amount))
                self.show_account_menu()
            else:
                messagebox.showerror("Error", "Invalid Password!")

        tk.Button(self.root, text="Withdraw", command=withdraw_money, font=font_settings).pack(pady=10)
        tk.Button(self.root, text="Back to Menu", command=self.show_account_menu, font=font_settings).pack(pady=10)

    def show_deposit(self):
        self.clear_window()
        
        font_settings = ("Helvetica", 25)
        font_headings = ("Helvetica",18)
        md_headings = ("Helvetica",35)
        
        tk.Label(self.root, text=f"Elevate Your Money Management with  ϻᴅ's A.T.M ༻", font=md_headings).pack(pady=10)

        tk.Label(self.root, text="Amount:", font=font_headings).pack()
        amount_entry = tk.Entry(self.root, font=font_headings)
        amount_entry.pack()

        tk.Label(self.root, text="Password:", font=font_headings).pack()
        password_entry = tk.Entry(self.root, show='*', font=font_headings)
        password_entry.pack()

        def deposit_money():
            amount = float(amount_entry.get())
            password = password_entry.get()
            if self.authenticate_user(self.current_user, password):
                messagebox.showinfo("Info", self.perform_deposit(amount))
                self.show_account_menu()
            else:
                messagebox.showerror("Error", "Invalid Password!")

        tk.Button(self.root, text="Deposit", command=deposit_money, font=font_settings).pack(pady=10)
        tk.Button(self.root, text="Back to Menu", command=self.show_account_menu, font=font_settings).pack(pady=10)

    def show_check_balance(self):
        self.clear_window()
        
        font_settings = ("Helvetica", 25)
        font_headings = ("Helvetica",18)
        md_headings = ("Helvetica",35)

        tk.Label(self.root, text=f"Track Your Financial Position with  ϻᴅ's A.T.M ༻", font=md_headings).pack(pady=10)

        balance = self.get_user_balance(self.current_user)
        balance_label = tk.Label(self.root, text=f"Current Balance: ₹{balance}", font=font_headings)
        balance_label.pack(pady=10)

        tk.Button(self.root, text="Back to Menu", command=self.show_account_menu, font=font_settings).pack(pady=10)

    def show_change_password(self):
        self.clear_window()
        
        font_settings = ("Helvetica", 25)
        font_headings = ("Helvetica",18)
        md_headings = ("Helvetica",35)
        
        tk.Label(self.root, text=f"Modify Your Access Credentials  ϻᴅ's A.T.M ༻", font=md_headings).pack(pady=10)

        tk.Label(self.root, text="Old Password:", font=font_headings).pack()
        old_password_entry = tk.Entry(self.root, show='*', font=font_headings)
        old_password_entry.pack()

        tk.Label(self.root, text="New Password:", font=font_headings).pack()
        new_password_entry = tk.Entry(self.root, show='*', font=font_headings)
        new_password_entry.pack()

        def change_password():
            old_password = old_password_entry.get()
            new_password = new_password_entry.get()
            if self.authenticate_user(self.current_user, old_password):
                self.update_user_password(self.current_user, new_password)
                messagebox.showinfo("Success", "Password changed successfully!")
                self.show_account_menu()
            else:
                messagebox.showerror("Error", "Invalid Password!")

        tk.Button(self.root, text="Change Password", command=change_password, font=font_settings).pack(pady=10)
        tk.Button(self.root, text="Back to Menu", command=self.show_account_menu, font=font_settings).pack(pady=10)

    def get_user(self, user_id):
        conn = self._connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user

    def authenticate_user(self, user_id, pin):
        user = self.get_user(user_id)
        return user and user[1] == pin

    def create_account(self, user_id, name, pin, balance=100, email='', phone_number='', address='', details=None):
        if details is None:
            details = ['', '', '']
        details_str = ','.join(details)
        conn = self._connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (user_id, pin, name, balance, email, phone_number, address, details) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (user_id, pin, name, balance, email, phone_number, address, details_str))
        conn.commit()
        conn.close()

    def update_user_balance(self, user_id, new_balance):
        conn = self._connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET balance=? WHERE user_id=?", (new_balance, user_id))
        conn.commit()
        conn.close()

    def update_user_password(self, user_id, new_pin):
        conn = self._connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET pin=? WHERE user_id=?", (new_pin, user_id))
        conn.commit()
        conn.close()

    def get_user_balance(self, user_id):
        user = self.get_user(user_id)
        return user[3] if user else 0

    def perform_withdrawal(self, amount):
        user = self.get_user(self.current_user)
        if user and user[3] >= amount:
            new_balance = user[3] - amount
            self.update_user_balance(self.current_user, new_balance)
            self.record_transaction(self.current_user, -amount, "Withdrawal")
            return f"Withdrawal successful! New Balance: ₹{new_balance}"
        return "Insufficient balance!"

    def perform_deposit(self, amount):
        user = self.get_user(self.current_user)
        if user:
            new_balance = user[3] + amount
            self.update_user_balance(self.current_user, new_balance)
            self.record_transaction(self.current_user, amount, "Deposit")
            return f"Deposit successful! New Balance: ₹{new_balance}"
        return "Error in deposit!"

    def perform_transfer(self, amount, recipient_user_id):
        user = self.get_user(self.current_user)
        recipient = self.get_user(recipient_user_id)
        if user and recipient and user[3] >= amount:
            new_balance = user[3] - amount
            self.update_user_balance(self.current_user, new_balance)
            recipient_new_balance = recipient[3] + amount
            self.update_user_balance(recipient_user_id, recipient_new_balance)
            self.record_transaction(self.current_user, -amount, "Transfer", recipient_user_id)
            self.record_transaction(recipient_user_id, amount, "Transfer", self.current_user)
            return f"Transfer successful! Your New Balance: ₹{new_balance}"
        return "Transfer failed! Check balance and recipient details."

    def record_transaction(self, user_id, amount, transaction_type, recipient_user_id=None):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = self._connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO transactions (user_id, amount, timestamp, type, recipient_user_id) VALUES (?, ?, ?, ?, ?)",
                       (user_id, amount, timestamp, transaction_type, recipient_user_id))
        conn.commit()
        conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = ATM(root)
    root.mainloop()
