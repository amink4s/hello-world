MYSQL_HOST = '127.0.0.1'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '1234'
MYSQL_DATABASE = 'student_db'

import mysql.connector
from mysql.connector import Error

# --- Tkinter UI Setup (Procedural Style) ---
import tkinter as tk
from tkinter import ttk

# Create main window
root = tk.Tk()
root.title("Student Database")

# Main error label (above buttons)
main_error_label = tk.Label(root, text="", fg="red")
main_error_label.grid(row=0, column=0, columnspan=4, pady=(10, 0))

# First Name
tk.Label(root, text="First Name:").grid(row=1, column=0, sticky="e")
first_name_entry = tk.Entry(root)
first_name_entry.grid(row=1, column=1)
first_name_error = tk.Label(root, text="", fg="red")
first_name_error.grid(row=1, column=2, sticky="w")

# Last Name
tk.Label(root, text="Last Name:").grid(row=2, column=0, sticky="e")
last_name_entry = tk.Entry(root)
last_name_entry.grid(row=2, column=1)
last_name_error = tk.Label(root, text="", fg="red")
last_name_error.grid(row=2, column=2, sticky="w")

# IDcode
tk.Label(root, text="IDcode:").grid(row=3, column=0, sticky="e")
idcode_entry = tk.Entry(root)
idcode_entry.grid(row=3, column=1)
idcode_error = tk.Label(root, text="", fg="red")
idcode_error.grid(row=3, column=2, sticky="w")

# Age
tk.Label(root, text="Age:").grid(row=4, column=0, sticky="e")
age_entry = tk.Entry(root)
age_entry.grid(row=4, column=1)
age_error = tk.Label(root, text="", fg="red")
age_error.grid(row=4, column=2, sticky="w")

# Phone
tk.Label(root, text="Phone:").grid(row=5, column=0, sticky="e")
phone_entry = tk.Entry(root)
phone_entry.grid(row=5, column=1)
phone_error = tk.Label(root, text="", fg="red")
phone_error.grid(row=5, column=2, sticky="w")

# Gender
tk.Label(root, text="Gender:").grid(row=6, column=0, sticky="e")
gender_var = tk.StringVar()
gender_male = tk.Radiobutton(root, text="Male", variable=gender_var, value="male")
gender_female = tk.Radiobutton(root, text="Female", variable=gender_var, value="female")
gender_male.grid(row=6, column=1, sticky="w")
gender_female.grid(row=6, column=1, sticky="e")
gender_error = tk.Label(root, text="", fg="red")
gender_error.grid(row=6, column=2, sticky="w")

# --- Button Logic (Procedural) ---
def validate_fields():
    """
    Checks all input fields and returns True if all are valid, otherwise False.
    Shows error messages next to fields if invalid.
    """
    valid = True
    # Clear previous error messages
    first_name_error.config(text="")
    last_name_error.config(text="")
    idcode_error.config(text="")
    age_error.config(text="")
    phone_error.config(text="")
    gender_error.config(text="")
    main_error_label.config(text="")

    # First Name
    first_name = first_name_entry.get().strip()
    if not first_name:
        first_name_error.config(text="Required")
        valid = False

    # Last Name
    last_name = last_name_entry.get().strip()
    if not last_name:
        last_name_error.config(text="Required")
        valid = False

    # IDcode
    idcode = idcode_entry.get().strip()
    if not (idcode.isdigit() and len(idcode) == 10):
        idcode_error.config(text="Must be 10 digits")
        valid = False

    # Age
    age = age_entry.get().strip()
    if not (age.isdigit() and 1 <= int(age) <= 100):
        age_error.config(text="Age 1-100")
        valid = False

    # Phone
    phone = phone_entry.get().strip()
    if not (phone.isdigit() and len(phone) == 11 and phone.startswith("09")):
        phone_error.config(text="Must be 11 digits, start with 09")
        valid = False

    # Gender
    gender = gender_var.get()
    if gender not in ["male", "female"]:
        gender_error.config(text="Required")
        valid = False

    return valid

def save():
    if not validate_fields():
        main_error_label.config(text="Please fix errors above.")
        return

    # Get field values
    first_name = first_name_entry.get().strip()
    last_name = last_name_entry.get().strip()
    idcode = idcode_entry.get().strip()
    age = int(age_entry.get().strip())
    phone = phone_entry.get().strip()
    gender = gender_var.get()

    # Connect to DB
    conn = get_db_connection()
    if not conn:
        main_error_label.config(text="Database connection error.")
        return
    cursor = conn.cursor()

    # Check if IDcode already exists
    cursor.execute("SELECT idcode FROM students WHERE idcode = %s", (idcode,))
    if cursor.fetchone():
        main_error_label.config(text="IDcode already exists.")
        cursor.close()
        conn.close()
        return

    # Insert new record
    try:
        cursor.execute(
            "INSERT INTO students (idcode, first_name, last_name, age, phone, gender) VALUES (%s, %s, %s, %s, %s, %s)",
            (idcode, first_name, last_name, age, phone, gender)
        )
        conn.commit()
        main_error_label.config(text="Record saved successfully!", fg="green")
        update_record_counter()
    except Exception as e:
        main_error_label.config(text=f"Error saving record: {e}")
    cursor.close()
    conn.close()

# Update the record counter label
def update_record_counter():
    conn = get_db_connection()
    if not conn:
        counter_label.config(text="Records: ?")
        return
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]
    counter_label.config(text=f"Records: {count}")
    cursor.close()
    conn.close()

def search():
    # Clear previous error messages
    first_name_error.config(text="")
    last_name_error.config(text="")
    idcode_error.config(text="")
    age_error.config(text="")
    phone_error.config(text="")
    gender_error.config(text="")
    main_error_label.config(text="")

    idcode = idcode_entry.get().strip()
    if not (idcode.isdigit() and len(idcode) == 10):
        idcode_error.config(text="Must be 10 digits")
        main_error_label.config(text="Enter a valid IDcode to search.")
        return

    conn = get_db_connection()
    if not conn:
        main_error_label.config(text="Database connection error.")
        return
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, last_name, age, phone, gender FROM students WHERE idcode = %s", (idcode,))
    result = cursor.fetchone()
    if result:
        first_name_entry.delete(0, tk.END)
        first_name_entry.insert(0, result[0])
        last_name_entry.delete(0, tk.END)
        last_name_entry.insert(0, result[1])
        age_entry.delete(0, tk.END)
        age_entry.insert(0, str(result[2]))
        phone_entry.delete(0, tk.END)
        phone_entry.insert(0, result[3])
        gender_var.set(result[4])
        main_error_label.config(text="Record found.", fg="green")
    else:
        main_error_label.config(text="Person not found.", fg="red")
    cursor.close()
    conn.close()

def delete():
    # Clear previous error messages
    first_name_error.config(text="")
    last_name_error.config(text="")
    idcode_error.config(text="")
    age_error.config(text="")
    phone_error.config(text="")
    gender_error.config(text="")
    main_error_label.config(text="")

    idcode = idcode_entry.get().strip()
    if not (idcode.isdigit() and len(idcode) == 10):
        idcode_error.config(text="Must be 10 digits")
        main_error_label.config(text="Enter a valid IDcode to delete.")
        return

    conn = get_db_connection()
    if not conn:
        main_error_label.config(text="Database connection error.")
        return
    cursor = conn.cursor()
    cursor.execute("SELECT idcode FROM students WHERE idcode = %s", (idcode,))
    if not cursor.fetchone():
        main_error_label.config(text="Person not found.", fg="red")
        cursor.close()
        conn.close()
        return

    try:
        cursor.execute("DELETE FROM students WHERE idcode = %s", (idcode,))
        conn.commit()
        main_error_label.config(text="Record deleted.", fg="green")
        update_record_counter()
        # Optionally clear fields after delete
        first_name_entry.delete(0, tk.END)
        last_name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        gender_var.set("")
    except Exception as e:
        main_error_label.config(text=f"Error deleting record: {e}")
    cursor.close()
    conn.close()

def edit():
    # Clear previous error messages
    first_name_error.config(text="")
    last_name_error.config(text="")
    idcode_error.config(text="")
    age_error.config(text="")
    phone_error.config(text="")
    gender_error.config(text="")
    main_error_label.config(text="")

    # Validate all fields except IDcode uniqueness
    if not validate_fields():
        main_error_label.config(text="Please fix errors above.")
        return

    idcode = idcode_entry.get().strip()
    first_name = first_name_entry.get().strip()
    last_name = last_name_entry.get().strip()
    age = int(age_entry.get().strip())
    phone = phone_entry.get().strip()
    gender = gender_var.get()

    conn = get_db_connection()
    if not conn:
        main_error_label.config(text="Database connection error.")
        return
    cursor = conn.cursor()
    cursor.execute("SELECT idcode FROM students WHERE idcode = %s", (idcode,))
    if not cursor.fetchone():
        main_error_label.config(text="Person not found.", fg="red")
        cursor.close()
        conn.close()
        return

    try:
        cursor.execute(
            "UPDATE students SET first_name=%s, last_name=%s, age=%s, phone=%s, gender=%s WHERE idcode=%s",
            (first_name, last_name, age, phone, gender, idcode)
        )
        conn.commit()
        main_error_label.config(text="Record updated.", fg="green")
        update_record_counter()
    except Exception as e:
        main_error_label.config(text=f"Error updating record: {e}")
    cursor.close()
    conn.close()

# Buttons at the bottom
save_btn = tk.Button(root, text="Save", width=10, command=save)
search_btn = tk.Button(root, text="Search", width=10, command=search)
delete_btn = tk.Button(root, text="Delete", width=10, command=delete)
edit_btn = tk.Button(root, text="Edit", width=10, command=edit)
save_btn.grid(row=8, column=0, pady=20)
search_btn.grid(row=8, column=1, pady=20)
delete_btn.grid(row=8, column=2, pady=20)
edit_btn.grid(row=8, column=3, pady=20)

# Record counter at the bottom
counter_label = tk.Label(root, text="Records: 0", fg="blue")
counter_label.grid(row=9, column=0, columnspan=4, pady=(0, 10))

# --- MySQL Table Creation ---

# --- MySQL Table Creation ---
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_table_if_not_exists():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                idcode VARCHAR(10) PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                age INT NOT NULL,
                phone VARCHAR(11) NOT NULL,
                gender ENUM('male', 'female') NOT NULL
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()

# Call this at the start of your program
create_table_if_not_exists()

# Start the Tkinter main loop
root.mainloop()
