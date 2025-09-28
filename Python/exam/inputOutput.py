name = input("Enter your name: ")
family = input("Enter your family name: ")

with open("name_list.txt", "a") as file:
    file.write(f"{name} {family}\n")
    print("Name and family name saved to name_list.txt")
    