import tkinter as tk
from tkinter import messagebox
from auth import register_user, login_user, get_user_data, update_user_data

class BankLoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Login System")
        self.root.geometry("300x300")
        self.create_login_page()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_login_page(self):
        self.clear_window()
        tk.Label(self.root, text="Login", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Login", command=self.login).pack(pady=10)
        tk.Button(self.root, text="Register", command=self.create_register_page).pack(pady=5)

    def create_register_page(self):
        self.clear_window()
        tk.Label(self.root, text="Register", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="New Username").pack()
        self.new_username = tk.Entry(self.root)
        self.new_username.pack(pady=5)

        tk.Label(self.root, text="New Password").pack()
        self.new_password = tk.Entry(self.root, show="*")
        self.new_password.pack(pady=5)

        tk.Button(self.root, text="Register", command=self.register).pack(pady=10)
        tk.Button(self.root, text="Back to Login", command=self.create_login_page).pack(pady=5)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        success, result = login_user(username, password)
        if success:
            messagebox.showinfo("Login Success", f"Welcome {username}!")
            self.open_dashboard(username)
        else:
            messagebox.showerror("Login Failed", result)

    def register(self):
        username = self.new_username.get().strip()
        password = self.new_password.get().strip()
        success, msg = register_user(username, password)
        if success:
            messagebox.showinfo("Success", msg)
            self.create_login_page()
        else:
            messagebox.showerror("Error", msg)

    def open_dashboard(self, username):
        self.current_user = username
        self.user_data = get_user_data(username)
        self.show_dashboard()

    def show_dashboard(self):
        self.clear_window()
        tk.Label(self.root, text=f"Welcome, {self.current_user}!", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text=f"Balance: ${self.user_data['balance']:.2f}", font=("Arial", 12)).pack(pady=5)

        tk.Button(self.root, text="Deposit", command=self.deposit_screen).pack(pady=5)
        tk.Button(self.root, text="Withdraw", command=self.withdraw_screen).pack(pady=5)
        tk.Button(self.root, text="Transaction History", command=self.show_transactions).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.create_login_page).pack(pady=10)

    def deposit_screen(self):
        self.clear_window()
        tk.Label(self.root, text="Enter amount to deposit:").pack()
        amount_entry = tk.Entry(self.root)
        amount_entry.pack()

        def deposit():
            try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    raise ValueError
                self.user_data['balance'] += amount
                self.user_data['transactions'].append(f"Deposited ${amount:.2f}")
                update_user_data(self.current_user, self.user_data)
                messagebox.showinfo("Success", f"${amount:.2f} deposited successfully!")
                self.show_dashboard()
            except ValueError:
                messagebox.showerror("Error", "Invalid amount")

        tk.Button(self.root, text="Deposit", command=deposit).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.show_dashboard).pack()

    def withdraw_screen(self):
        self.clear_window()
        tk.Label(self.root, text="Enter amount to withdraw:").pack()
        amount_entry = tk.Entry(self.root)
        amount_entry.pack()

        def withdraw():
            try:
                amount = float(amount_entry.get())
                if amount <= 0 or amount > self.user_data['balance']:
                    raise ValueError
                self.user_data['balance'] -= amount
                self.user_data['transactions'].append(f"Withdrew ${amount:.2f}")
                update_user_data(self.current_user, self.user_data)
                messagebox.showinfo("Success", f"${amount:.2f} withdrawn successfully!")
                self.show_dashboard()
            except ValueError:
                messagebox.showerror("Error", "Invalid amount or insufficient funds")

        tk.Button(self.root, text="Withdraw", command=withdraw).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.show_dashboard).pack()

    def show_transactions(self):
        self.clear_window()
        tk.Label(self.root, text="Transaction History", font=("Arial", 14)).pack(pady=10)

        if self.user_data["transactions"]:
            for t in self.user_data["transactions"][-10:][::-1]:
                tk.Label(self.root, text=t).pack()
        else:
            tk.Label(self.root, text="No transactions yet.").pack()

        tk.Button(self.root, text="Back", command=self.show_dashboard).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = BankLoginApp(root)
    root.mainloop()
