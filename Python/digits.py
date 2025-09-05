number=int(input("enter a number: "))

i = 0
while True:
    if number/10**i < 1:
        break
    i = i + 1
    
print(f"{number} has {i} digits")