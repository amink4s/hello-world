number1 = int(input("enter the first number "))
number2 = int(input("enter the second number "))
number3 = int(input("enter the last number "))

if number1 < number2 and number1 < number3:
    smallest = number1
    if number2 < number3:
        middle = number2
        largest = number3
    else:
        middle = number3
        largest = number2

elif number2 < number1 and number2 < number3:
    smallest = number2
    if number3 < number1:
        middle = number3
        largest = number1
    else:
        middle = number1
        largest = number3
else:
    smallest = number3
    if number2 < number3:
        middle = number2
        largest = number3
    else:
        middle = number3
        largest = number2
print(f"{smallest},{middle},{largest}")