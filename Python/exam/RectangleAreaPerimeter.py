while True:
    try:
        num1 = int(input("Please enter the first number: "))
        num2 = int(input("Please enter the second number: ")) 

        if num1 >= 0 and num2 >= 0:
            break  # Input is valid, exit the while loop

        else:
            print("Error: The sides of a rectangle cannot be negative. Please enter non-negative numbers only.")
            
    except ValueError:
        print("Error: Invalid input. Please ensure you enter a whole number.")

square = (num1 == num2)
area = num1 * num2
perimeter = (num1 + num2) * 2

print(f"perimeter is {perimeter} and area is {area}")

if square:
    print("this is also a square!")