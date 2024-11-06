import tkinter as tk
from tkinter import messagebox
import mysql.connector

# MySQL database connection settings
db_config = {
    'user': 'root',
    'password': 'COM@45PASS',
    'host': 'localhost',
    'database': 'shruti'
}

# Function to open the customer form
def open_customer_form():
    customer_window = tk.Toplevel(root)
    customer_window.title("Customer Form")
    customer_window.geometry("400x400")

    # Frame for the customer form with a border and background color
    frame_customer = tk.Frame(customer_window, bd=1, relief=tk.RIDGE, bg='light yellow')
    frame_customer.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Customer Form Title
    label_title = tk.Label(frame_customer, text="Customer Entry Form", font=("Arial", 22), bg='light blue')
    label_title.pack(pady=10)

    # Customer ID
    label_cid = tk.Label(frame_customer, text="Customer ID:", font=("Arial", 18), bg='light yellow')
    label_cid.pack(pady=5)
    entry_cid = tk.Entry(frame_customer)
    entry_cid.pack(pady=5)

    # Customer Name
    label_cname = tk.Label(frame_customer, text="Customer Name:", font=("Arial", 18), bg='light yellow')
    label_cname.pack(pady=5)
    entry_cname = tk.Entry(frame_customer)
    entry_cname.pack(pady=5)

    # Phone Number
    label_phno = tk.Label(frame_customer, text="Phone Number:", font=("Arial", 18), bg='light yellow')
    label_phno.pack(pady=5)
    entry_phno = tk.Entry(frame_customer)
    entry_phno.pack(pady=5)

    # Address
    label_address = tk.Label(frame_customer, text="Address:", font=("Arial", 18), bg='light yellow')
    label_address.pack(pady=5)
    entry_address = tk.Entry(frame_customer)
    entry_address.pack(pady=5)

    # Dues
    label_dues = tk.Label(frame_customer, text="Dues:", font=("Arial", 18), bg='light yellow')
    label_dues.pack(pady=5)
    entry_dues = tk.Entry(frame_customer)
    entry_dues.pack(pady=5)

    # Function to clear the form
    def new_customer():
        entry_cid.delete(0, tk.END)
        entry_cname.delete(0, tk.END)
        entry_phno.delete(0, tk.END)
        entry_address.delete(0, tk.END)
        entry_dues.delete(0, tk.END)

    # Function to update customer data in MySQL
    def update_customer():
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            sql = "UPDATE customers SET cname=%s, phno=%s, address=%s, dues=%s WHERE cid=%s"
            values = (entry_cname.get(), entry_phno.get(), entry_address.get(), entry_dues.get(), entry_cid.get())
            cursor.execute(sql, values)
            conn.commit()
            messagebox.showinfo("Customer Updated", f"Customer {entry_cname.get()} updated successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            cursor.close()
            conn.close()

    # Function to delete customer data from MySQL
    def delete_customer():
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            sql = "DELETE FROM customers WHERE cid=%s"
            cursor.execute(sql, (entry_cid.get(),))
            conn.commit()
            messagebox.showinfo("Customer Deleted", "Customer deleted successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            cursor.close()
            conn.close()

    # Function to save customer data to MySQL
    def save_customer():
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            sql = "INSERT INTO customers (cname, phno, address, dues) VALUES (%s, %s, %s, %s)"
            values = (entry_cname.get(), entry_phno.get(), entry_address.get(), entry_dues.get())
            cursor.execute(sql, values)
            conn.commit()
            messagebox.showinfo("Customer Saved", f"Customer {entry_cname.get()} saved successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            cursor.close()
            conn.close()

    # Function to open a search form
    def open_search_form():
        search_window = tk.Toplevel(customer_window)
        search_window.title("Search Customer")
        search_window.geometry("300x200")

        label_search = tk.Label(search_window, text="Enter Customer ID:", font=("Arial", 16))
        label_search.pack(pady=10)
        entry_search_cid = tk.Entry(search_window)
        entry_search_cid.pack(pady=10)

        # Function to search for the customer and display details
        def search_customer():
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                sql = "SELECT cname, phno, address, dues FROM customers WHERE cid=%s"
                cursor.execute(sql, (entry_search_cid.get(),))
                result = cursor.fetchone()
                if result:
                    result_window = tk.Toplevel(search_window)
                    result_window.title("Customer Details")
                    result_window.geometry("400x200")

                    label_result = tk.Label(result_window, text="Customer Details", font=("Arial", 18))
                    label_result.pack(pady=10)

                    label_name = tk.Label(result_window, text=f"Name: {result[0]}", font=("Arial", 14))
                    label_name.pack(pady=5)
                    label_phone = tk.Label(result_window, text=f"Phone: {result[1]}", font=("Arial", 14))
                    label_phone.pack(pady=5)
                    label_address = tk.Label(result_window, text=f"Address: {result[2]}", font=("Arial", 14))
                    label_address.pack(pady=5)
                    label_dues = tk.Label(result_window, text=f"Dues: {result[3]}", font=("Arial", 14))
                    label_dues.pack(pady=5)
                else:
                    messagebox.showinfo("Search Result", "No customer found with this ID.")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", str(err))
            finally:
                cursor.close()
                conn.close()

        button_search_submit = tk.Button(search_window, text="Search", command=search_customer)
        button_search_submit.pack(pady=10)

    # Save button
    button_save = tk.Button(frame_customer, text="Save", command=save_customer, bg='light blue', width=20, height=3)
    button_save.pack(side=tk.LEFT, padx=30)

    # New button
    button_new = tk.Button(frame_customer, text="New", command=new_customer, bg='light blue', width=20, height=3)
    button_new.pack(side=tk.LEFT, padx=30)

    # Update button
    button_update = tk.Button(frame_customer, text="Update", command=update_customer, bg='light blue', width=20, height=3)
    button_update.pack(side=tk.LEFT, padx=30)

    # Delete button
    button_delete = tk.Button(frame_customer, text="Delete", command=delete_customer, bg='light blue', width=20, height=3)
    button_delete.pack(side=tk.LEFT, padx=30)

    # Search button (opens search form)
    button_search = tk.Button(frame_customer, text="Search", command=open_search_form, bg='light blue', width=20, height=3)
    button_search.pack(side=tk.LEFT, padx=30)


# Function to handle login
def login():
    username = entry_username.get()
    password = entry_password.get()

    # Hardcoded verification (replace with database logic as needed)
    if username == "admin" and password == "password":
        messagebox.showinfo("Login Successful", "Welcome!")
        open_customer_form()  # Open customer form on successful login
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Create the main window
root = tk.Tk()
root.title("Login Form")
root.geometry("500x600")

# Frame for the login form with a border and background color
frame_login = tk.Frame(root, bd=10, relief=tk.RIDGE, bg='light blue')
frame_login.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Login Form Title
label_title = tk.Label(frame_login, text="Login Form", font=("Arial", 20), bg='light yellow')
label_title.pack(pady=10)

# Username Label and Entry
label_username = tk.Label(frame_login, text="Username:", font=("Arial", 16), bg='light yellow')
label_username.pack(pady=5)
entry_username = tk.Entry(frame_login)
entry_username.pack(pady=5)

# Password Label and Entry
label_password = tk.Label(frame_login, text="Password:", font=("Arial", 16), bg='light yellow')
label_password.pack(pady=5)
entry_password = tk.Entry(frame_login, show="*")
entry_password.pack(pady=5)

# Login Button
button_login = tk.Button(frame_login, text="Login", command=login)
button_login.pack(pady=10)

# Start the GUI event loop
root.mainloop()