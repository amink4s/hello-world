import sqlite3

conn = sqlite3.connect('names.db')  
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT, 
        last_name TEXT
    )
''')

for i in range(10):
    first_name = input(f"Enter first name for student {i+1}/10: ")
    last_name = input(f"Enter last name for student {i+1}/10: ")
    cursor.execute('INSERT INTO students (first_name, last_name) VALUES (?, ?)', (first_name, last_name))
conn.commit()
print("10 student records saved.\n")

search_last_name = input("Enter the last name to search for: ")
cursor.execute('SELECT first_name, last_name FROM students WHERE last_name = ?', (search_last_name,))
results = cursor.fetchall()
if results:
    print("Search Results:")
    for first_name, last_name in results:
        print(f"Found: {first_name} {last_name}")
else:
    print("No students found with that last name.")

update_last_name = input("Enter the last name of the student you want to update: ")
new_first_name = input("Enter the new first name: ")

cursor.execute('UPDATE students SET first_name = ? WHERE last_name = ?', (new_first_name, update_last_name))

if cursor.rowcount > 0:
    print(f"Success: {cursor.rowcount} record(s) with last name '{update_last_name}' updated to '{new_first_name}'.")
else:
    print("No student found with that last name. No changes made.")

conn.commit()
conn.close()