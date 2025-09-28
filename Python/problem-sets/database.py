import mysql.connector
from mysql.connector import Error

# Database connection configuration
config = {
    'host': 'localhost',
    'user': 'root',
    'password': '', # Replace with your password
    'database': 'testdb' # Replace with your database name
}

def connect_db():
    """Establish connection to MySQL database."""
    try:
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            print("Successfully connected to the database.")
            return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_table_if_not_exists(conn):
    """Create employees table if it doesn't exist."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                family_name VARCHAR(255) NOT NULL,
                personal_id VARCHAR(20) NOT NULL,
                age INT NOT NULL
            )
        """)
        conn.commit()
        print("Table 'employees' is ready.")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()

def add_data(conn):
    """Add a new employee record."""
    try:
        cursor = conn.cursor()
        name = input("Enter name: ")
        family_name = input("Enter family name: ")
        personal_id = input("Enter personal ID (e.g., SSN): ")
        age = int(input("Enter age: "))
        cursor.execute("INSERT INTO employees (name, family_name, personal_id, age) VALUES (%s, %s, %s, %s)", (name, family_name, personal_id, age))
        conn.commit()
        print("Employee added successfully.")
    except Error as e:
        print(f"Error adding data: {e}")
    except ValueError:
        print("Invalid age value. Please enter an integer.")
    finally:
        cursor.close()

def delete_data(conn):
    """Delete an employee record by ID."""
    try:
        cursor = conn.cursor()
        emp_id = int(input("Enter employee ID to delete: "))
        cursor.execute("DELETE FROM employees WHERE id = %s", (emp_id,))
        if cursor.rowcount > 0:
            conn.commit()
            print("Employee deleted successfully.")
        else:
            print("No employee found with that ID.")
    except Error as e:
        print(f"Error deleting data: {e}")
    except ValueError:
        print("Invalid ID. Please enter an integer.")
    finally:
        cursor.close()

def edit_data(conn):
    """Edit an employee record by ID."""
    try:
        cursor = conn.cursor()
        emp_id = int(input("Enter employee ID to edit: "))
        # Check if ID exists
        cursor.execute("SELECT * FROM employees WHERE id = %s", (emp_id,))
        if cursor.fetchone() is None:
            print("No employee found with that ID.")
            return
        
        print("Leave blank to keep current value.")
        name = input("Enter new name (or press Enter to skip): ") or None
        family_name = input("Enter new family name (or press Enter to skip): ") or None
        personal_id = input("Enter new personal ID (or press Enter to skip): ") or None
        age_input = input("Enter new age (or press Enter to skip): ")
        age = int(age_input) if age_input else None
        
        updates = []
        params = []
        if name:
            updates.append("name = %s")
            params.append(name)
        if family_name:
            updates.append("family_name = %s")
            params.append(family_name)
        if personal_id:
            updates.append("personal_id = %s")
            params.append(personal_id)
        if age is not None:
            updates.append("age = %s")
            params.append(age)
        
        if updates:
            params.append(emp_id)
            query = f"UPDATE employees SET {', '.join(updates)} WHERE id = %s"
            cursor.execute(query, params)
            conn.commit()
            print("Employee updated successfully.")
        else:
            print("No changes made.")
    except Error as e:
        print(f"Error editing data: {e}")
    except ValueError:
        print("Invalid age value. Please enter an integer.")
    finally:
        cursor.close()

def query_data(conn):
    """Query and display all employee records."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees")
        rows = cursor.fetchall()
        if rows:
            print("\nEmployee Records:")
            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]}, Family Name: {row[2]}, Personal ID: {row[3]}, Age: {row[4]}")
        else:
            print("No records found.")
        print()
    except Error as e:
        print(f"Error querying data: {e}")
    finally:
        cursor.close()

def main():
    """Main program loop."""
    conn = connect_db()
    if not conn:
        return
    
    create_table_if_not_exists(conn)
    
    while True:
        print("\nOptions: add, delete, edit, query, q (quit)")
        choice = input("Enter your choice: ").lower().strip()
        
        if choice == 'q':
            print("Exiting program.")
            break
        elif choice == 'add':
            add_data(conn)
        elif choice == 'delete':
            delete_data(conn)
        elif choice == 'edit':
            edit_data(conn)
        elif choice == 'query':
            query_data(conn)
        else:
            print("Invalid choice. Please try again.")
    
    if conn.is_connected():
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()